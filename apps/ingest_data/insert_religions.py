import csv
from apps.utils import error
from apps.db import queries
from apps.db.DBHandler import DBHandler

CSV_PATH = '../../data/csv/'


def parse_religion_csv(dbh, file):
    with open(CSV_PATH + file) as csv_file:
        reader = csv.reader(csv_file)
        next(reader)

        for row in reader:
            name = row[1].split(" ")
            religion = row[2]
            first_name = name[0]
            last_name = " "
            last_name = last_name.join(name[1:]).strip()
            vals = (last_name, first_name)

            res = dbh.query_db(
                queries.get_member_id_by_first_last_name(),
                vals)

            if not res or len(res) > 1:

                res = dbh.query_db(
                    queries.get_member_id_by_first_last_name_in_office(),
                    vals)

                if res:
                    member_id = res[0]
            else:
                member_id = res[0]

            if last_name == "" and first_name == "":
                member_id = 'R000576'

            if member_id:
                dbh.write_to_db(
                    queries.update_religion(),
                    (religion, member_id))



def main():
    dbh = DBHandler()
    parse_religion_csv(dbh, 'member_religions.csv')
    dbh.commit()
    dbh.close()
    print("MOC religions added to db!")


if __name__ == "__main__":
    main()
