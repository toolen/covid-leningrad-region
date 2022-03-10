"""This file contains utility functions."""
from datetime import datetime
from typing import Dict, Optional, Union
from urllib.parse import ParseResult, urlparse

from scraper.exceptions import ImproperlyConfiguredException


def get_date_from_str(date: str, format_: str = "%d.%m.%y") -> datetime:
    """
    Covert string to datetime.

    :param date: date as string.
    :param format_: format string.
    :return: None
    """
    return datetime.strptime(date, format_)


def email_url(url: Optional[str]) -> Dict[str, Union[str, int, bool]]:
    """
    Parse url to dict.

    :param url: url string of email server.
    :return: Dict of connection parameters.
    """
    if url:
        login = ""
        password = ""  # nosec
        parse_result: ParseResult = urlparse(url)
        scheme = parse_result.scheme
        netloc = parse_result.netloc
        if scheme and netloc:
            if "@" in netloc:
                netloc_splitted = netloc.split("@")

                if len(netloc_splitted) == 2:
                    creds, host = netloc.split("@")
                else:
                    host = netloc_splitted.pop()
                    creds = "@".join(netloc_splitted)

                if creds and ":" in creds:
                    login, password = creds.split(":")
            else:
                host = netloc

            host, port = host.split(":")

            return {
                "EMAIL_HOST": host,
                "EMAIL_PORT": int(port),
                "EMAIL_USE_SSL": scheme == "smtp+ssl",
                "EMAIL_HOST_USER": login,
                "EMAIL_HOST_PASSWORD": password,
            }
    raise ImproperlyConfiguredException(f"Invalid email url {url}")


def avoid_empty_value(value: Optional[str]) -> str:
    """
    Rise ImproperlyConfiguredException if value is empty.

    :param value: any value.
    :return: value if not empty.
    """
    if value:
        return value
    else:
        raise ImproperlyConfiguredException()
