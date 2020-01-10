import os
import psycopg2
from configparser import ConfigParser
from apps.utils.error import error
from apps.db import queries


class DBHandler:

    def __init__(self, conf='database.ini', site_root=os.environ['VIRTUAL_ENV']):
        self.config_filepath = str(site_root) + str(conf)
        self.db_params = self.parse_config(self.config_filepath)
        self.conn, self.cur = self.init_connection()

    def init_connection(self):
        try:
            conn = psycopg2.connect(**self.db_params)
            cur = conn.cursor()
        except psycopg2.DatabaseError as de:
            error(de)
            return None

        return conn, cur

    def parse_config(self, section='postgres'):
        parser = ConfigParser()
        db_params = {}

        try:
            parser.read(self.config_filepath)

            if parser.has_section(section):
                params = parser.items(section)

                for param in params:
                    db_params[param[0]] = param[1]
        except IOError as io:
            error(io)
        except KeyError as ke:
            error(ke)

        return db_params

    def write_to_db(self, sql, params, return_key=False):
        """
        Execute an insert, update, or create statement.
        :param sql: sql query string, with %s as placeholder for parameter values
        :param params: NoneType or tuple of query parameters, must equal amount specified in query.
        :return: If your query has a RETURNING CLAUSE, returns value[0] of tuple returned by db, else
        NoneType.
        """
        if not check_query_params(sql, params):
            return

        try:
            if len(params) == 0:
                self.cur.execute(sql)
            else:
                self.cur.execute(sql, params)

            if return_key:
                # Do I want to be handing back the entire tuple? I think in this case no, it's a
                # newly generated id retrieval.
                record_id = self.conn.fetchone()[0]
            else:
                record_id = None

            self.conn.commit()
            return record_id
        except ConnectionError as e:
            error(e)

    def query_db(self, sql, params=None, fetch_one=False):
        """
        Execute any sql query providing return results.
        :param sql: sql query string, with %s as placeholder for parameter values
        :param params: Defaults to None (no parameters specified). NoneType or tuple
        of query parameters. Must equal amount specified in query.
        :param fetch_one: Defaults to False (fetch all results). if True, only returns
        one (first or only) result row.
        If False, returns all results supplied by db.
        :return: NoneType if no results. Tuple if fetch_one=True and db returned result.
        Otherwise, list of tuples.
        """
        if not check_query_params(sql, params=None):
            return
        try:
            self.cur.execute(sql, params)

            if fetch_one:
                res = self.conn.fetchone()
            else:
                res = self.conn.fetchall()

            self.conn.commit()
            return res if res else None
        except ConnectionError as e:
            error(e)

    def close(self):
        """
        Close database connection.
        :return:
        """
        self.cur.close()
        self.conn.close()

    def get_mem_id_by_name(self, last_name, first_name=None):
        """
        Retrieves currently in office MOC's member_id by first and last name
        :param last_name: last_name as string
        :param first_name: first_name as string, optional.
        :return: member_id if exists, else None
        """
        if last_name and first_name:
            sql = queries.get_member_id_by_first_last_name()
            query_params = (last_name, first_name)
        else:
            sql = queries.get_member_id_by_last_name()
            query_params = (last_name,)

        member_ids = self.query_db(sql, query_params)

        return validate_id_res(member_ids)

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

        if not last_name or len(last_name) == 0 or type(last_name) != str or \
                not state or len(state) != 2 or type(state) != str:
            print("Last name and state are required. Both should be strings, and state should "
                  "be 2 characters")
            raise ValueError

        last_name = last_name.capitalize()
        state = state.upper()
        session = int(session)
        district = int(district)

        if session and type(session) != int or district and type(district) != int:
            print("if providing a session or district, they must be a valid integer.")
            raise ValueError
        if not district and not session:
            res = self.query_db(queries.mem_id_by_name_state(), (last_name, state))
        elif not district:
            res = self.query_db(queries.mem_id_by_name_session_state(), (last_name, state, session))
        elif not session:
            res = self.query_db(queries.mem_id_by_name_state_district(),
                                (last_name, state, district))
        else:
            res = self.query_db(queries.mem_id_by_name_session_state_district(),
                                (last_name, state, session, district))

        return validate_id_res(res)


def validate_id_res(ids):
    if len(ids) == 0:
        print("No matching ids found")
    elif len(ids) > 1:
        print("Multiple possible matches returned, "
              "please narrow your search by adding more criteria.")
    else:
        if len(ids[0]) == 0 or len(ids[0]) > 1:
            print("""
                The result tuple was an invalid length (should be 
                length 1). Illegal return condition. It wasn't you, 
                it was me.
                """)
            raise psycopg2.InternalError
        else:
            return ids[0][0]
    return None


def check_query_params(sql, query_params=None):
    if type(sql) != str or (query_params and type(query_params) != tuple):
        print("TypeError: Type of query is: " + type(sql))
        print("Type of parameter values is: " + type(query_params))
        raise TypeError
    if not sql or sql == "":
        raise psycopg2.ProgrammingError
    elif type(sql) != str or type(query_params) != tuple:
        raise TypeError
    else:
        param_count = sql.count("%s")

        if (not query_params or len(query_params) == 0) and param_count != 0 or \
                len(query_params) != param_count:
            print("Expected param count:" + str(param_count) + ", actual: " + str(len(query_params)))
            print(sql + " --> " + query_params)
            raise psycopg2.OperationalError
    return True





