"""This file contains utility functions."""
from datetime import datetime


def get_date_from_str(date: str) -> datetime:
    """
    Covert string to datetime.

    :param date:
    :return:
    """
    return datetime.strptime(date, "%d.%m.%y")
