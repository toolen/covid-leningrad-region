"""This file is entrypoint of application."""
import logging
import signal
import sys
import time
from types import FrameType
from typing import cast
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

import schedule

from scraper.config import (DB_COLLECTION_NAME, DB_NAME, DB_URI, TLS_CA_PATH,
                            TLS_CERT_KEY_PATH, URL)
from scraper.db import DBWrapper
from scraper.decorators import retry_on_failure
from scraper.exceptions import InvalidURLException
from scraper.parsers import CovidPageParser

logging.basicConfig(
    stream=sys.stdout,
    level=logging.DEBUG,
    format="[%(levelname)s %(asctime)s %(name)s] %(message)s",
)
logger = logging.getLogger(__name__)
is_active = True


@retry_on_failure()
def get_html_page(url: str) -> str:
    """
    Return HTML page by url.

    :param url:
    :return:
    """
    if url.startswith("http://") or url.startswith("https://"):
        req = Request(url)
        try:
            response = urlopen(req, timeout=500)  # nosec
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

    :return:
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
            logger.error("HTML is None!")
    except BaseException as e:
        logger.error(e)
    finally:
        logger.info("Job done.")


def graceful_shutdown(signals: signal.Signals, frame_type: FrameType) -> None:
    """
    Cleanup application before shutdown.

    :return:
    """
    global is_active
    is_active = False


def main() -> None:
    """
    Start application.

    :return:
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
