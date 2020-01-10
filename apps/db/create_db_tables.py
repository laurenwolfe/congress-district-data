import psycopg2
from apps.db import create_queries
from apps.utils import error
import os

db_params = "host=localhost dbname=congress_data user=congress_data password=TestPass port=32768"
conn = psycopg2.connect(db_params)
cur = conn.cursor()


def query_db(sql):
    try:
        cur.execute(sql)
    except ConnectionError as e:
        error.log_error(e)


def create_tables(build_flag=False):
    if not build_flag:
        print("Not creating db tables, build_flag False")
        return

    query_db(create_queries.create_district())
    query_db(create_queries.create_alter_district())
    query_db(create_queries.create_member())
    query_db(create_queries.create_member_district())
    query_db(create_queries.create_member_house())
    query_db(create_queries.create_member_senate())
    query_db(create_queries.create_member_id_url())
    query_db(create_queries.create_member_session())
    query_db(create_queries.create_district_summary())
    query_db(create_queries.create_district_poverty_summary())
    query_db(create_queries.create_district_poverty_detail())
    # not yet added, want to think about the structure
    # query_db(queries.create_house_expenditure())

    conn.commit()
    cur.close()
    conn.close()


def main():
    create_tables()     # Must pass True to activate function


if __name__ == "__main__":
    main()
