from apps.db.DBHandler import DBHandler
from apps.db import queries
from apps.ingest_data import insert_district_ids, insert_members
from time import sleep


def main():
    # dbh = DBHandler()
    # dbh.write_to_db(queries.truncate_all(), None)
    # dbh.commit()
    # dbh.close()
    # sleep(5)
    # insert_district_ids.main()
    insert_members.main()


if __name__ == "__main__":
    main()
