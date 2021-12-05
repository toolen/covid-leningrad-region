from datetime import datetime

from scraper.utils import get_date_from_str


def test_get_date_from_str():
    value_as_str = "14.10.21"
    value_as_datetime: datetime = get_date_from_str(value_as_str)

    assert value_as_datetime.day == 14
    assert value_as_datetime.month == 10
    assert value_as_datetime.year == 2021
    assert value_as_datetime.hour == 0
    assert value_as_datetime.minute == 0
    assert value_as_datetime.second == 0
    assert value_as_datetime.microsecond == 0
