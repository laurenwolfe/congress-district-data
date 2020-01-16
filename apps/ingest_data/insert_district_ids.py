import csv
from apps.db import queries
from apps.db.DBHandler import DBHandler

CSV_PATH = '../../data/csv/'


def insert_district_ids(dbh, file, update_members=False):
    """
    Add districts to db
    :param dbh: database querying object of type DBHandler
    :param file: csv file containing (state, district) tuples
    :param update_members: If True, assigns district_ids to house member records
    """

    with open(CSV_PATH + file) as csv_file:
        reader = csv.reader(csv_file)

        for row in reader:
            district_id = dbh.write_to_db(queries.insert_district_id(), (row[0], int(row[1])), True)

            if not district_id:
                raise dbh.NoDataFound

            if update_members:
                dbh.write_to_db(queries.set_member_session_district_id(),
                                (district_id, row[0], row[1]), False)
    print("Added districts to member records!")


def main():
    dbh = DBHandler()
    insert_district_ids(dbh, 'districts.csv')
    dbh.close()


if __name__ == "__main__":
    main()

