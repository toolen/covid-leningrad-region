import json
import os
from datetime import datetime
from typing import Any

import pytest

from scraper.config import (DB_COLLECTION_NAME, DB_NAME, DB_URI, TLS_CA_PATH,
                            TLS_CERT_KEY_PATH)
from scraper.db import DBWrapper


@pytest.fixture
def db():
    print(DB_URI)
    db = DBWrapper(
        DB_URI, f"{DB_NAME}_test", DB_COLLECTION_NAME, TLS_CERT_KEY_PATH, TLS_CA_PATH
    )
    yield db
    db.drop_collection()
    db.close()


@pytest.fixture
def path_to_files_dir():
    return os.path.join(os.path.dirname(os.path.realpath(__file__)), "files")


def date_parser(dct):
    if "date" in dct:
        dct["date"] = datetime.strptime(dct["date"], "%Y-%m-%d")
    return dct


class CustomEncoder(json.JSONEncoder):
    def default(self, o: Any) -> Any:
        if isinstance(o, datetime):
            return str(o)[:10]
        return super().default(o)
