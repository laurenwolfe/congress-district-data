import csv
from apps.utils import data
from apps.db import queries
from apps.db.DBHandler import DBHandler

CSV_PATH = '../../data/csv/'
CURR_SESSION = '116'


def parse_member_csv(file, dbh):
    with open(CSV_PATH + file) as csv_file:
        reader = csv.reader(csv_file)
        next(reader)
        for row in reader:
            state = row[1]
            district_num = row[2]
            last_name = row[3]

            if not district_num:
                member_id = dbh.query_db(
                    queries.get_member_id_by_state_last_name(),
                    (CURR_SESSION, None, state, last_name))
            else:
                district_id = dbh.query_db(
                    queries.get_district(), (state, district_num))
                district_id = district_id[0]

                member_id = dbh.query_db(
                    queries.get_member_id_by_current_district(), (district_id,))

            print(row)
            member_id = member_id[0]
            race_eth = row[9].split(' - ')

            if len(race_eth) >= 1:
                race = race_eth[0]
                races = race.split("/")
                race_1 = races[0] if len(races) >= 1 else None
                race_2 = races[1] if len(races) == 2 else None

            if len(race_eth) == 2:
                ethnicity = race_eth[1]
                ethnicities = ethnicity.split("/")
                ethnicity_1 = ethnicities[0] if len(ethnicities) >= 1 else None
                ethnicity_2 = ethnicities[1] if len(ethnicities) == 2 else None

            full_name = row[5]
            lgbtq = row[10]
            presidential_results = row[11:17]
            senate_election_res = row[17:21]
            house_election_res = row[21:27]
            demographics = row[45:]

            member_vals = data.convert_to_tuple(
                [full_name, race_1, ethnicity_1, race_2, ethnicity_2,
                 lgbtq, member_id])

            dbh.write_to_db(queries.update_member_demos(), member_vals)

            if row[0] == 'rep':
                demographic_vals = demographics + presidential_results + [district_id]
                demographic_vals = data.convert_to_tuple(demographic_vals)
                dbh.write_to_db(queries.update_district_summary(), demographic_vals)
                house_vals = house_election_res + [member_id]
                house_vals = data.convert_to_tuple(house_vals)
                dbh.write_to_db(queries.update_member_house(), house_vals)
            elif row[0] == 'sen':
                senate_vals = senate_election_res + [member_id]
                senate_vals = data.convert_to_tuple(senate_vals)
                dbh.write_to_db(queries.update_member_senate(), senate_vals)
            else:
                raise LookupError


def main():
    dbh = DBHandler()
    parse_member_csv('116th_congress.csv', dbh)
    dbh.commit()
    dbh.close()


if __name__ == "__main__":
    main()
