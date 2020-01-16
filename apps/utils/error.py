import sys
from datetime import datetime


def log_error(e):
    """ Print and exit when an exception is thrown.
    :param e: message returned by system
    :return: none, exit
    """
    error_output = "{} - Error message: {} \n".format(datetime.now(), e)
    f = open("../logs/easy_data_err_log.txt", "a")
    f.write(error_output)
    f.close()
    sys.exit(error_output)


def error(e):
    log_error(e)
