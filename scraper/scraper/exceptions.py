"""This file contains exceptions classes."""


class ScraperException(Exception):
    """Base class for application exceptions."""

    pass


class InvalidURLException(Exception):
    """The url does not specify http or https protocol."""

    pass


class ImproperlyConfiguredException(Exception):
    """Some config property value is empty or invalid."""

    pass
