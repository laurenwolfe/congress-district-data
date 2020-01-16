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

            sql = """
                SELECT id from member
                where last_name = %s and first_name = %s;            
            """

            vals = (name[1], name[0])

            res = dbh.execute(sql, vals)
            print(name)
            print(res)

            # res = dbh.get_mem_id_by_name((last_name, first_name))

            '''

                possible_names.append((last_name, first_name))
            else:
                if len(name) < 2:
                    continue

                first_name = name[0]
                last_name_1 = name[1]
                last_name_2 = name[2]
                last_name_3 = name[1] + " " + name[2]

                possible_names.append((last_name_1, first_name))
                possible_names.append((last_name_2, first_name))
                possible_names.append((last_name_3, first_name))

            for name in possible_names:
                

                if res:
                    dbh.write_to_db(queries.update_religion(), (religion, res))
                    break
            '''


def main():
    dbh = DBHandler()
    parse_religion_csv(dbh, 'member_religions.csv')
    dbh.commit()
    dbh.close()


if __name__ == "__main__":
    main()
