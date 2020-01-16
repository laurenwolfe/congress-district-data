import csv
import psycopg2
from apps.utils import error, data
from apps.ingest import get_member_id, queries

CSV_PATH = '../data/csv/'
CURR_SESSION = '116'

db_params = "dbname=house-spending user=house-spending port=5431"
conn = psycopg2.connect(db_params)
cur = conn.cursor()


def parse_member_csv(file):
    with open(CSV_PATH + file) as csv_file:
        reader = csv.reader(csv_file)
        next(reader)

        for row in reader:
            lookup_result = get_member_id.by_session_state_last_name(
                # session, district, state, last_name
                [CURR_SESSION, row[2], row[1], row[3]])
            member_id = lookup_result[0] if lookup_result else None

            if not member_id:
                raise LookupError

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
            demographics = row[51:]

            member_vals = [full_name, race_1, ethnicity_1, race_2,
                           ethnicity_2, lgbtq, member_id]

            query_db(queries.update_member,
                     tuple(data.convert_empty_to_null(member_vals)))

            demographic_vals = demographics + presidential_results + [member_id]

            query_db(queries.update_demographics,
                     tuple(data.convert_empty_to_null(demographic_vals)))

            if row[0] == 'rep':
                house_vals = house_election_res + [member_id]
                query_db(queries.update_member_house,
                         tuple(data.convert_empty_to_null(house_vals)))
            elif row[0] == 'sen':
                senate_vals = senate_election_res + [member_id]
                query_db(queries.update_member_senate,
                         tuple(data.convert_empty_to_null(senate_vals)))
            else:
                raise LookupError


def query_db(sql, vals):
    try:
        cur.execute(sql, vals)
        conn.commit()
    except ConnectionError as e:
        error.log_error(e)
    except TypeError as te:
        error.log_error(te)


def main():
    parse_member_csv('116th_congress.csv')
    conn.commit()
    cur.close()
    conn.close()


if __name__ == "__main__":
    main()
