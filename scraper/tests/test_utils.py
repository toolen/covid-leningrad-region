from datetime import datetime
from uuid import uuid4

import pytest

from scraper.exceptions import ImproperlyConfiguredException
from scraper.utils import email_url, get_date_from_str


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


def test_email_url():
    with pytest.raises(ImproperlyConfiguredException):
        email_url(None)

    with pytest.raises(ImproperlyConfiguredException):
        email_url("")

    with pytest.raises(ImproperlyConfiguredException):
        email_url(uuid4().hex)

    with pytest.raises(ImproperlyConfiguredException):
        email_url("example.com")

    assert email_url("smtp://example.com:25") == {
        "EMAIL_HOST": "example.com",
        "EMAIL_PORT": 25,
        "EMAIL_USE_SSL": False,
        "EMAIL_HOST_USER": "",
        "EMAIL_HOST_PASSWORD": "",
    }

    assert email_url("smtp://@example.com:25") == {
        "EMAIL_HOST": "example.com",
        "EMAIL_PORT": 25,
        "EMAIL_USE_SSL": False,
        "EMAIL_HOST_USER": "",
        "EMAIL_HOST_PASSWORD": "",
    }

    assert email_url("smtp://:@example.com:25") == {
        "EMAIL_HOST": "example.com",
        "EMAIL_PORT": 25,
        "EMAIL_USE_SSL": False,
        "EMAIL_HOST_USER": "",
        "EMAIL_HOST_PASSWORD": "",
    }

    assert email_url("smtp://user:pass@example.com:25") == {
        "EMAIL_HOST": "example.com",
        "EMAIL_PORT": 25,
        "EMAIL_USE_SSL": False,
        "EMAIL_HOST_USER": "user",
        "EMAIL_HOST_PASSWORD": "pass",
    }

    assert email_url("smtp+ssl://user:pass@example.com:25") == {
        "EMAIL_HOST": "example.com",
        "EMAIL_PORT": 25,
        "EMAIL_USE_SSL": True,
        "EMAIL_HOST_USER": "user",
        "EMAIL_HOST_PASSWORD": "pass",
    }

    assert email_url("smtp+ssl://user@example.com:pass@example.com:25") == {
        "EMAIL_HOST": "example.com",
        "EMAIL_PORT": 25,
        "EMAIL_USE_SSL": True,
        "EMAIL_HOST_USER": "user@example.com",
        "EMAIL_HOST_PASSWORD": "pass",
    }
