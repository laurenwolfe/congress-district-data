import requests
from apps.utils import error


def download_files(base_url, filenames, dest_path):
    for filename in filenames:
        file_dest = dest_path + filename
        file_src = base_url + filename

        try:
            r = requests.get(file_src)

            with open(file_dest, 'w') as f:
                f.write(r.content)

            # Retrieve HTTP meta-data
            print(r.status_code)
            print(r.headers['content-type'])
            print(r.encoding)
        except ConnectionError as ce:
            error(ce)
        except PermissionError as pe:
            error(pe)

        print("Successfully downloaded" + file_src +" to " + file_dest)


def generate_file_names(start_year, start_qtr, end_year, end_qtr, suffix):
    quarters = ['Q1', 'Q2', 'Q3', 'Q4']
    start_qtr_idx = start_qtr - 1
    end_qtr_idx = end_qtr - 1

    file_list = []

    for year in range(end_year, start_year, -1):
        for i in range(len(quarters)):
            if year == start_year and start_qtr_idx > i:
                continue
            if year == end_year and i > end_qtr_idx:
                continue
            file_list.append(str(year) + quarters[i] + suffix)
    return file_list


def main():
    file_list = generate_file_names(2008, 1, 2019, 4, '-house-disburse-detail.csv')
    base_url = 'https://projects.propublica.org/congress/assets/staffers/'
    dest_path = '../../data/csv/financial/'

    download_files(base_url, file_list, dest_path)


if __name__ == "__main__":
    main()

# TODO: CONVERT TO REST QUERIES
