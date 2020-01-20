from time import sleep

from apps.db.DBHandler import DBHandler
from apps.db import queries, create_db_tables
from apps.ingest_data import insert_district_ids, insert_members, \
    insert_demographics, insert_religions, insert_census_poverty


def main():

    dbh = DBHandler()
    dbh.write_to_db(queries.drop_all(), None)
    dbh.commit()
    dbh.close()
    print("Dropped Tables!")

    create_db_tables.main()
    print("DB Tables created!")
    insert_district_ids.main()
    print("Districts created!")
    insert_members.main()
    print("Members created!")
    insert_demographics.main()
    print("Demographics inserted!")
    insert_religions.main()
    print("Religions inserted!")
    insert_census_poverty.main()
    print("Poverty data inserted!")


if __name__ == "__main__":
    main()
