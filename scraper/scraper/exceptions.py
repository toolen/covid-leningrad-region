"""This file contains exceptions classes."""


class ScraperException(Exception):
    """Base class for application exceptions."""

    pass


class InvalidURLException(ScraperException):
    """The url does not specify http or https protocol."""

    pass


class ImproperlyConfiguredException(ScraperException):
    """Some config property value is empty or invalid."""

    pass


class NoCurrentDateException(ScraperException):
    """Scraper failed to get current date from html page."""

    pass


class CurrentDatesNotMatchException(ScraperException):
    """Dates from title and table are different."""

    pass
