import csv
from apps.db import queries
from apps.ingest_data import mappings
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
        state_to_fips = {value: key for key, value in mappings.states.items()}

        """
        Backwards fix, should be integrated for new build
        for row in reader:
            dbh.write_to_db("UPDATE district set state_fips = %s where state = %s;",
                            (int(state_to_fips[row[0]]), row[0]))

        """
        for row in reader:
            district_id = dbh.write_to_db(
                queries.insert_district_id(),
                (row[0], int(row[1]), int(state_to_fips[row[0]])),
                True)

            if not district_id:
                raise dbh.NoDataFound

            if update_members:
                dbh.write_to_db(queries.set_member_session_district_id(),
                                (district_id, row[0], row[1]), False)



    print("Added districts to member records!")


def main():
    dbh = DBHandler()
    insert_district_ids(dbh, 'districts.csv')
    dbh.commit()
    dbh.close()


if __name__ == "__main__":
    main()

