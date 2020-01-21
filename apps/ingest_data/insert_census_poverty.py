import csv
from apps.ingest_data import mappings
from apps.db import queries
from apps.db.DBHandler import DBHandler
from apps.utils import data

CSV_PATH = '../../data/csv/'


def parse_csv(files, years, year_idxs_list, dbh):
    for i in range(len(files)):
        with open(CSV_PATH + files[i]) as csv_file:
            reader = csv.reader(csv_file)
            next(reader)

            for row in reader:
                # include_idx index 0 should always refer to the index of the district_code in csv file
                district_code_idx = year_idxs_list[i][0]
                data_idxs = year_idxs_list[i][2:]
                district_code = row[district_code_idx]
                district_id = extract_district_id(district_code, dbh)

                included_cells = [district_id, years[i]]

                for idx in data_idxs:
                    included_cells.append(data.convert_census_null_to_0(row[idx]))

                dt = included_cells
                if files[i] == 'ACSST1Y2014.S1701.csv':
                    summary_vals = (
                        dt[0], dt[1], dt[2], dt[27], dt[28],
                        dt[29], dt[30], dt[31], None, None,
                        None
                    )
                    # associated values stored as idxs 3 - 26
                    detail_total_vals = (
                        dt[0], dt[1], False, dt[2], dt[3],
                        dt[4], dt[5], dt[6], dt[7], dt[8],
                        dt[9], dt[10], dt[11], dt[12], dt[13],
                        dt[14], dt[15], dt[16], dt[17], dt[18],
                        dt[19], dt[20], dt[21], dt[22], dt[23],
                        dt[24], dt[25], dt[26]
                    )
                    # associated values stored as idxs 32 - 56
                    # only have data on population living at 200 % of poverty level and below for this year
                    detail_poverty_vals = (
                        dt[0], dt[1], True, dt[32], dt[33],
                        dt[34], dt[35], dt[36], dt[37], dt[38],
                        dt[39], dt[40], dt[41], dt[42], dt[43],
                        dt[44], dt[45], dt[46], dt[47], dt[48],
                        dt[49], dt[50], dt[51], dt[52], dt[53],
                        dt[54], dt[55], dt[56]
                    )
                else:
                    summary_vals = (
                        dt[0], dt[1], dt[2], dt[27], dt[28],
                        dt[29], dt[30], dt[31], dt[32], dt[33],
                        dt[34]
                    )
                    # associated values stored as idxs 3 - 26
                    detail_total_vals = (
                        dt[0], dt[1], False, dt[2], dt[3],
                        dt[4], dt[5], dt[6], dt[7], dt[8],
                        dt[9], dt[10], dt[11], dt[12], dt[13],
                        dt[14], dt[15], dt[16], dt[17], dt[18],
                        dt[19], dt[20], dt[21], dt[22], dt[23],
                        dt[24], dt[25], dt[26]
                    )
                    # associated values stored as idxs 35 - 59
                    # note that there's an offset here, due to the additional data on
                    # of population living at 300, 400, 500 % of poverty level included in summary
                    detail_poverty_vals = (
                        dt[0], dt[1], True, dt[35], dt[36],
                        dt[37], dt[38], dt[39], dt[40], dt[41],
                        dt[42], dt[43], dt[44], dt[45], dt[46],
                        dt[47], dt[48], dt[49], dt[50], dt[51],
                        dt[52], dt[53], dt[54], dt[55], dt[56],
                        dt[57], dt[58], dt[59]
                    )

                dbh.write_to_db(queries.insert_poverty_summ(), summary_vals)
                dbh.write_to_db(queries.insert_poverty_details(), detail_total_vals)
                dbh.write_to_db(queries.insert_poverty_details(), detail_poverty_vals)


def extract_district_id(census_code, dbh):
    loc_data = census_code.split("US")
    loc_id = loc_data[1]

    # lookup state abbreviation based on 2 digit key assigned by census bureau
    state = mappings.states[loc_id[0:2]]
    district = int(loc_id[2:])

    # district 98 is code for non-voting delegate, which I've coded as 0 (same as at-large)
    if district == 98:
        district = 0

    district_id = dbh.query_db(queries.get_district(), (state, district))

    if not district_id:
        raise KeyError
    else:
        return district_id


def list_headers(files, headers):
    for i in range(len(files)):
        with open(CSV_PATH + files[i]) as csv_file:
            reader = csv.reader(csv_file)

            for cols in reader:
                j = 0
                for idx in headers[i]:
                    print(str(j), cols[idx])
                    j += 1
                break

            """
            for cols in reader:
                j = 0
                for col in cols:
                    print(str(j), col)
                    j += 1
                break
            """


def main():
    dbh = DBHandler()

    parse_csv(
        ['ACSST1Y2014.S1701.csv', 'ACSST1Y2015.S1701_old.csv', 'ACSST1Y2016.S1701.csv', 'ACSST1Y2017.S1701.csv', 'ACSST1Y2018.S1701.csv'],
        ['2014', '2015', '2016', '2017', '2018'],
        [mappings.census_poverty_idxs_2014, mappings.census_poverty_idxs_2015, mappings.census_poverty_idxs_2016_2017,
         mappings.census_poverty_idxs_2016_2017, mappings.census_poverty_idxs_2018],
        dbh
    )
    dbh.commit()
    dbh.close()


if __name__ == "__main__":
    main()
