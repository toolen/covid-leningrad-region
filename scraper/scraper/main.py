import logging
import sys
import time
import urllib.request
from typing import cast
from urllib.error import URLError

import schedule

from scraper.config import (DB_COLLECTION_NAME, DB_NAME, DB_URI, TLS_CA_PATH,
                            TLS_CERT_KEY_PATH, URL)
from scraper.db import DBWrapper
from scraper.decorators import retry_on_failure
from scraper.parsers import CovidPageParser

logging.basicConfig(
    stream=sys.stdout,
    level=logging.DEBUG,
    format="[%(levelname)s %(asctime)s %(name)s] %(message)s",
)
logger = logging.getLogger(__name__)


@retry_on_failure()
def get_html_page(url: str) -> str:
    try:
        with urllib.request.urlopen(url, timeout=500) as response:
            return cast(str, response.read().decode("utf-8"))
    except URLError as e:
        logger.error(e)
        raise e


def job() -> None:
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


def main() -> None:
    logger.info("Scraper started.")

    job()
    schedule.every().hour(job)
    while True:
        schedule.run_pending()
        time.sleep(1)


if __name__ == "__main__":
    main()
