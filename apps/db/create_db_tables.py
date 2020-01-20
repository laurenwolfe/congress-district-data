from apps.db import create_queries
from apps.db.DBHandler import DBHandler


def create_tables(dbh, build_flag=False):
    if not build_flag:
        print("Not creating db tables, build_flag False")
        return

    dbh.query_db(create_queries.create_district())
    dbh.query_db(create_queries.create_alter_district())
    dbh.query_db(create_queries.create_member())
    dbh.query_db(create_queries.create_member_district())
    dbh.query_db(create_queries.create_member_house())
    dbh.query_db(create_queries.create_member_senate())
    dbh.query_db(create_queries.create_member_id_url())
    dbh.query_db(create_queries.create_member_session())
    dbh.query_db(create_queries.create_district_summary())
    dbh.query_db(create_queries.create_district_poverty_summary())
    dbh.query_db(create_queries.create_district_poverty_detail())
    # not yet added, want to think about the structure
    # query_db(queries.create_house_expenditure())

    dbh.commit()
    dbh.close()


def main():
    dbh = DBHandler()
    create_tables(dbh, True)     # Must pass True to activate function


if __name__ == "__main__":
    main()
