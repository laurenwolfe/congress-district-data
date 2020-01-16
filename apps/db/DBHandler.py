import os
import psycopg2
from configparser import ConfigParser
from apps.utils.error import error
from apps.db import queries


class DBHandler:

    def __init__(self, conf='database.ini', site_root=os.environ['VIRTUAL_ENV']):
        self.conf = conf
        self.site_root = site_root
        self.config_filepath = None
        self.conn = None
        self.cur = None
        self.init_connection()

    def init_connection(self):
        db_params = self.parse_config()

        try:
            self.conn = psycopg2.connect(**db_params)
            self.cur = self.conn.cursor()
        except psycopg2.DatabaseError as de:
            error(de)

    def parse_config(self, section='postgres'):
        parser = ConfigParser()
        postgres_config_params = {}

        try:
            parser.read(self.site_root + "/" + self.conf)
            if not parser.has_section(section):
                raise KeyError

            for param in parser.items(section):
                postgres_config_params[param[0]] = param[1]
        except IOError as io:
            error(io)

        return postgres_config_params

    def execute(self, sql, vals):
        self.cur.execute(sql, vals)

        if self.cur.rowcount > 0:
            return self.cur.fetchall()

    def write_to_db(self, sql, params, return_key=False):
        """
        Execute an insert, update, or create statement.
        :param sql: sql query string, with %s as placeholder for parameter values
        :param params: NoneType or tuple of query parameters, must equal amount specified in query.
        :param return_key: if True, queries the database to retrieve value fetched by RETURNING CLAUSE of sql param.
        :return: If your query has a RETURNING CLAUSE and return_key flag is set to True, returns value[0] of
        tuple returned by db, else NoneType.
        """
        try:
            if not params:
                self.cur.execute(sql)
            else:
                self.cur.execute(sql, params)

            self.conn.commit()

            if return_key:
                res = self.cur.fetchone()
                return res
        except ConnectionError as e:
            error(e)

    def query_db(self, sql, params=None, fetch_one=False):
        """
        Execute any sql query providing return results.
        :param sql: sql query string, with %s as placeholder for parameter values
        :param params: Defaults to None (no parameters specified). NoneType or tuple
        of query parameters. Must equal amount specified in query.
        :param fetch_one: Defaults to False (fetch all results). if True, only returns
        one (first or only) result row. If False, returns all results supplied by db.
        :return: NoneType if no results. Tuple if fetch_one=True and db returned result.
        Otherwise, list of tuples.
        """
        try:
            self.cur.execute(sql, params)

            row_count = self.cur.rowcount

            if row_count <= 0:
                res = None
            elif row_count == 1:
                res = self.cur.fetchone()
                self.conn.commit()
            else:
                res = self.cur.fetchall()
                self.conn.commit()
            return res

        except ConnectionError as e:
            error(e)

    def commit(self):
        self.conn.commit()

    def close(self):
        """
        Close database connection.
        :return:
        """
        self.cur.close()
        self.conn.close()

    def get_mem_id_by_name(self, params):
        """
        Retrieves currently in office MOC's member_id by first and last name
        :param last_name: last_name as string
        :param first_name: first_name as string, optional.
        :return: member_id if exists, else None
        """
        if len(params) > 1:
            query = queries.get_member_id_by_first_last_name()
        else:
            query = queries.get_member_id_by_last_name()

        self.cur.execute(query, params)

        res = self.cur.fetchone()

        if res:
            print(res)
            return res[0][0]
        else:
            print("no result")
        return None

    def get_mem_id_by_region(self, last_name, state, session=None, district=None):
        """
        :param last_name: member's last_name as string
        :param state: member's represented state (2-letter abbreviation)
        :param session: optional. Int session of congress when member served (optional, can help narrow
        in cases of parent/child political legacies
        :param district: optional. If in House of Reps, an int number representing their
        district within the state.
        :return: member_id if exists, else None
        """

        if not last_name or not state or (type(last_name) or type(state)) != str:
            print("Last name and state are required. Both should be strings, "
                  "and state should be 2 characters")
            raise ValueError

        last_name = last_name.capitalize()
        state = state.upper()
        session = int(session)
        district = int(district)

        if session and type(session) != int or district and type(district) != int:
            print("if providing a session or district, they must be a valid integer.")
            raise ValueError
        if not (district and session):
            res = self.query_db(queries.mem_id_by_name_state(),
                                (last_name, state), True)
        elif not district:
            res = self.query_db(queries.mem_id_by_name_session_state(),
                                (last_name, state, session))
        elif not session:
            res = self.query_db(queries.mem_id_by_name_state_district(),
                                (last_name, state, district))
        else:
            res = self.query_db(queries.mem_id_by_name_session_state_district(),
                                (last_name, state, session, district))

        return validate_id_res(res)


def validate_id_res(ids):
    if not ids:
        print("No matching ids found")
        return None
    elif len(ids) > 1:
        print("Multiple possible matches returned, "
              "please narrow your search by adding more criteria.")
        return None
    else:
        if len(ids[0]) != 1:
            print("""The result tuple was an invalid length (should be length 1). Illegal return condition. 
            It wasn't you, it was me.""")
            raise psycopg2.InternalError
        return ids[0][0]


def check_query_and_params(sql, query_params=None):
    if type(sql) != str or not sql:
        print("TypeError: Type of query is: " + str(type(sql)))
        raise TypeError
    if not query_params:
        return True

    if type(query_params) != tuple:
        print("Type of parameter values is: " + str(type(query_params)))
        raise TypeError

    param_count = sql.count("%s")

    if len(query_params) != param_count:
        print("Expected param count:" + str(param_count) + ", actual: " + str(len(query_params)))
        print(sql)
        print(query_params)
        raise psycopg2.OperationalError

    return True





