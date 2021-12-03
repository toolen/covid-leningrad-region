import json
import os

from scraper.constants import (PROPERTY_DISTRICT, PROPERTY_DISTRICT_DATE,
                               PROPERTY_DISTRICT_LOCALITIES,
                               PROPERTY_LOCALITY_NUMBER_OF_INFECTIONS)
from scraper.db import DBWrapper
from tests.conftest import date_parser


def test_save_data_idempotency(path_to_files_dir, db: DBWrapper):
    with open(os.path.join(path_to_files_dir, "page.json"), "r") as json_file:
        json_data = json_file.read()
        data = json.loads(json_data, object_hook=date_parser)

    for _ in range(3):
        db.save_data(data)
        assert db.collection_size() == len(data)


def test_save_data_with_updates(path_to_files_dir, db: DBWrapper):
    with open(os.path.join(path_to_files_dir, "page.json"), "r") as json_file:
        json_data = json_file.read()
        data = json.loads(json_data, object_hook=date_parser)

        db.save_data(data)
        assert db.collection_size() == len(data)

        old_value = data[0][PROPERTY_DISTRICT_LOCALITIES][0][
            PROPERTY_LOCALITY_NUMBER_OF_INFECTIONS
        ]
        new_value = old_value + 1
        data[0][PROPERTY_DISTRICT_LOCALITIES][0][
            PROPERTY_LOCALITY_NUMBER_OF_INFECTIONS
        ] = new_value
        db.save_data(data)
        assert db.collection_size() == len(data)

        collection = db.get_collection()
        result = collection.find_one(
            {
                PROPERTY_DISTRICT_DATE: data[0][PROPERTY_DISTRICT_DATE],
                PROPERTY_DISTRICT: data[0][PROPERTY_DISTRICT],
            }
        )
        value = result[PROPERTY_DISTRICT_LOCALITIES][0][
            PROPERTY_LOCALITY_NUMBER_OF_INFECTIONS
        ]
        assert value == new_value


def test_save_data_unique_by_date(path_to_files_dir, db):
    with open(os.path.join(path_to_files_dir, "page.json"), "r") as json_file:
        json_data = json_file.read()
        data = json.loads(json_data, object_hook=date_parser)

    with open(
        os.path.join(path_to_files_dir, "page_next_day.json"), "r"
    ) as next_json_file:
        next_json_data = next_json_file.read()
        data_next_day = json.loads(next_json_data, object_hook=date_parser)

    assert len(data) == 3
    assert len(data_next_day) == 3

    db.save_data(data)
    assert db.collection_size() == len(data)

    db.save_data(data_next_day)
    expected_document_count = len(data) + len(data_next_day)
    assert db.collection_size() == expected_document_count
