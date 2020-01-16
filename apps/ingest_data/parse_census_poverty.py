import csv
import psycopg2
from apps.ingest_data import mappings
from apps.db import queries
from apps.utils import data, error

CSV_PATH = '../data/csv/'

db_params = "dbname=house-spending user=house-spending port=5431"
conn = psycopg2.connect(db_params)
cur = conn.cursor()


def parse_csv(files, years, year_idxs_list):
    for i in range(len(files)):
        with open(CSV_PATH + files[i]) as csv_file:
            reader = csv.reader(csv_file)
            next(reader)

            for row in reader:
                # include_idx index 0 should always refer to the index of the district_code in csv file
                district_code = year_idxs_list[i][0]
                district_id = extract_district_id(district_code)

                included_cells = [years[i], district_id]

                for idx in year_idxs_list[i][1:]:
                    included_cells.append(data.convert_census_null_to_0(row[idx]))

                dt = included_cells

                summary_vals = (dt[1], dt[0], dt[28], dt[29], dt[30], dt[31], dt[32], dt[3])
                query_db(queries.insert_poverty_summ, summary_vals)

                detail_total_vals = (dt[1], dt[0], False,
                                     dt[3], dt[4], dt[5], dt[6], dt[7],
                                     dt[8], dt[9], dt[10], dt[11], dt[12],
                                     dt[13], dt[14], dt[15], dt[16], dt[17],
                                     dt[18], dt[19], dt[20], dt[21], dt[22],
                                     dt[23], dt[24], dt[25], dt[26], dt[27])
                query_db(queries.insert_poverty_details, detail_total_vals)

                detail_pov_vals = (dt[1], dt[0], True,
                                   dt[33], dt[34], dt[35], dt[36], dt[37],
                                   dt[38], dt[39], dt[40], dt[41], dt[42],
                                   dt[43], dt[44], dt[45], dt[46], dt[47],
                                   dt[48], dt[49], dt[50], dt[51], dt[52],
                                   dt[53], dt[54], dt[55], dt[56], dt[57])
                query_db(queries.insert_poverty_details, detail_pov_vals)


def extract_district_id(census_code):
    loc_id = census_code.split("US")[1]

    # lookup state abbreviation based on 2 digit key assigned by census bureau
    state = mappings.states[loc_id[0:2]]
    district = int(loc_id[2:])

    district_id = query_db(queries.get_district(), (state, district))

    if district_id:
        raise KeyError
    else:
        return district_id


def query_db(sql, vals):
    try:
        cur.execute(sql, vals)
        return cur.fetchone()
    except ConnectionError as e:
        error.log_error(e)


def main():
    parse_csv(
        [
            'ACSST1Y2014.S1701.csv',
            'ACSST1Y2016.S1701.csv',
            'ACSST1Y2017.S1701.csv',
            'ACSST1Y2018.S1701.csv'],
        ['2014', '2016', '2017', '2018'],
        [
            mappings.census_poverty_idxs_2014,
            mappings.census_poverty_idxs_2016_2017,
            mappings.census_poverty_idxs_2016_2017,
            mappings.census_poverty_idxs_2018
        ]
    )

    conn.commit()
    cur.close()
    conn.close()


if __name__ == "__main__":
    main()
