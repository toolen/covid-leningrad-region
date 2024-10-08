"""This file contains the code for working with the database."""

import logging
from typing import Dict, List, Optional, Union, cast

from pymongo import MongoClient, UpdateOne
from pymongo.collection import Collection
from pymongo.errors import BulkWriteError
from tenacity import retry, wait_fixed

from scraper.constants import PROPERTY_DISTRICT, PROPERTY_DISTRICT_DATE
from scraper.types import DistrictType

logger = logging.getLogger(__name__)


class DBWrapper:
    """This class provides methods for working with the database."""

    def __init__(
        self,
        uri: str,
        db_name: str,
        collection_name: str,
        tls_cert_key_path: Optional[str] = None,
        tls_ca_path: Optional[str] = None,
    ) -> None:
        """
        Construct the DBWrapper class.

        :param uri: connection string
        :param db_name: database name
        :param collection_name: collection name
        :param tls_cert_key_path: path to TLS key certificate
        :param tls_ca_path: path to CA certificate
        """
        tls: Dict[str, Union[bool, str]] = {}
        if tls_cert_key_path:
            tls["tls"] = True
            tls["tlsCertificateKeyFile"] = tls_cert_key_path
            if tls_ca_path:
                tls["tlsCAFile"] = tls_ca_path

        self.db_name = db_name
        self.collection_name = collection_name
        self.client = self.get_client(uri, tls)

    @retry(wait=wait_fixed(5))
    def get_client(self, uri: str, tls: Dict[str, Union[bool, str]]) -> MongoClient:
        """
        Return MongoClient instance.

        :param uri: connection string.
        :param tls: TLS options.
        :return: MongoClient instance.
        """
        return MongoClient(
            uri,
            connectTimeoutMS=1000,
            retryWrites=True,
            maxPoolSize=50,
            wTimeoutMS=2500,
            **tls
        )

    def get_collection(self) -> Collection:
        """
        Return default collection from database.

        :return: Collection
        """
        return self.client[self.db_name][self.collection_name]

    def drop_collection(self) -> None:
        """
        Drop default collection.

        :return: None
        """
        collection = self.get_collection()
        collection.drop()

    def collection_size(self) -> int:
        """
        Return size of default collection.

        :return: None
        """
        collection = self.get_collection()
        return cast(int, collection.estimated_document_count())

    def close(self) -> None:
        """
        Close database connection.

        :return: None
        """
        self.client.close()

    def save_data(self, data: List[DistrictType]) -> None:
        """
        Save data into database.

        :param data: data to save.
        :return: None
        """
        operations = []
        for district in data:
            filter_ = {
                PROPERTY_DISTRICT_DATE: district[PROPERTY_DISTRICT_DATE],
                PROPERTY_DISTRICT: district[PROPERTY_DISTRICT],
            }
            operations.append(UpdateOne(filter_, {"$set": district}, upsert=True))

        try:
            collection = self.get_collection()
            collection.bulk_write(operations)
            logger.info("Write success.")
        except BulkWriteError as bwe:
            logger.error(bwe.details)
