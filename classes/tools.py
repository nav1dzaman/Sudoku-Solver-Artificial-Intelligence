
import datetime


def get_human_readable_time(start_time, end_time):

    return str(datetime.timedelta(seconds=(end_time - start_time)))


def count_duplicates(arr):
    # Size of the given array minus the size of unique elements found in this array = nb of duplicates
    return len(arr) - len(set(arr))