from dateutil import parser
import re


def convert_empty_to_null(record):
    for field in record:
        if field == "":
            record[field] = None
    return record


def convert_to_tuple(record):
    record_list = []
    for field in record:
        if field == "":
            field = None
        record_list.append(field)
    return tuple(record_list)


def convert_census_null_to_0(record):
    for i in range(len(record)):
        if record[i] == "":
            record[i] = None
    return record


def convert_to_postgres_date(value, year=None):
    """
    This will convert a date in almost any format to one that postgres can happily insert into a DATE field.
    If no year is included (MM-DD, for instance), the parser fills in the current year. If that's not what you want,
    passing the (optional) year parameter will replace that default result.
    :param value:
    :param year: Optional 4-digit int representing a year value
    :return:
    """

    date_time = parser.parse(value)

    if year:
        date_time = date_time.replace(year)

    return date_time.date()


def to_currency(value):
    return format(float(value), '.2f')


def strip_non_numeric(value):
    return re.sub(r'[^\d.]+', '', value).strip()


def strip_year_prefix(value):
    if len(value) > 4 and value[0:4].isnumeric():
        value = value[5:len(value)]

    return value.strip()


def normalize_expenditure_string(value):
    """Removes: special characters, extra tabs and spacing, most punctuation for the sake of being able
        to combine matching records with character variations. Also converts to title case.

    :param value: unprocessed data value from csv
    :return: normalized data value
    """

    char_list = ['.', ',', '\t', '¬', '≠', '!', '?', '=']

    # remove characters from the given list
    table = value.maketrans('', '', ''.join(char_list))
    res_value = value.translate(table)

    amp_pattern = re.compile(r'\s*&\s*')
    bslash_pattern = re.compile(r"\s*\\\s*")
    fslash_pattern = re.compile(r"\s*/\s*")

    res_value = amp_pattern.sub(r"&", res_value)
    res_value = bslash_pattern.sub(r"\\", res_value)
    res_value = fslash_pattern.sub(r"/", res_value)
    normed_value = " ".join(res_value.split())
    normed_value = normed_value.title()

    return normed_value
