"""This file is entrypoint of application."""

import logging
import signal
import ssl
import sys
import time
from datetime import datetime
from types import FrameType
from typing import Optional, cast
from urllib.error import HTTPError, URLError
from urllib.parse import ParseResult, urlparse
from urllib.request import Request, urlopen

import certifi
import schedule
from tenacity import retry, wait_fixed

from scraper.config import (
    DB_COLLECTION_NAME,
    DB_NAME,
    DB_URI,
    TLS_CA_PATH,
    TLS_CERT_KEY_PATH,
    URL,
)
from scraper.db import DBWrapper
from scraper.exceptions import InvalidURLException, NoCurrentDateException
from scraper.mail import send_message_to_admin
from scraper.parsers import CovidPageParser

logging.basicConfig(
    stream=sys.stdout,
    level=logging.DEBUG,
    format="[%(levelname)s %(asctime)s %(name)s] %(message)s",
)
logger = logging.getLogger(__name__)
is_active = True


@retry(wait=wait_fixed(5))
def get_html_page(url: str) -> str:
    """
    Return HTML page by url.

    :param url: html page url.
    :return: HTML page as text.
    """
    parse_result: ParseResult = urlparse(url)
    if parse_result.scheme in (
        "http",
        "https",
    ):
        req = Request(url)
        context = None
        if parse_result.scheme == "https":
            context = ssl.create_default_context(cafile=certifi.where())
        try:
            response = urlopen(req, timeout=500, context=context)  # nosec
            return cast(str, response.read().decode("utf-8"))
        except HTTPError as e:
            logger.error(e)
            raise e
        except URLError as e:
            logger.error(e)
            raise e
    else:
        raise InvalidURLException()


def job() -> None:
    """
    Parse HTML page and save data into database.

    :return: None
    """
    logger.info("Run job.")
    try:
        html: str = get_html_page(URL)
        if html:
            parser = CovidPageParser()
            result = parser.parse(html)
            result.pop()  # exclude summary

            db = DBWrapper(
                DB_URI, DB_NAME, DB_COLLECTION_NAME, TLS_CERT_KEY_PATH, TLS_CA_PATH
            )
            db.save_data(result)
            db.close()
        else:
            msg = "Failed to get HTML page."
            logger.error(msg)
            send_message_to_admin(msg)
        logger.info("Job done.")
    except NoCurrentDateException as e:
        if 0 <= datetime.now().hour <= 10:
            # at this time, the page is usually not updated yet,
            # so the date on the page will not match the current date.
            pass
        else:
            logger.error(e)
            send_message_to_admin(str(e))
    except BaseException as e:
        logger.error(e)
        send_message_to_admin(str(e))


def graceful_shutdown(signum: int, frame: Optional[FrameType]) -> None:
    """
    Cleanup application before shutdown.

    :return: None
    """
    global is_active
    is_active = False


def main() -> None:
    """
    Start application.

    :return: None
    """
    logger.info("Scraper started.")

    signal.signal(signal.SIGTERM, graceful_shutdown)
    signal.signal(signal.SIGHUP, graceful_shutdown)
    signal.signal(signal.SIGINT, graceful_shutdown)

    # Run on startup
    job()

    schedule.every().hour.do(job)
    while is_active:
        schedule.run_pending()
        time.sleep(1)


if __name__ == "__main__":
    main()
