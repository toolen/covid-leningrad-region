"""This file contains database wrapper."""
import logging
from typing import Dict, List, Optional, Union, cast

from aiohttp import web
from motor.core import AgnosticClient
from motor.motor_asyncio import (
    AsyncIOMotorClient,
    AsyncIOMotorCollection,
    AsyncIOMotorDatabase,
)
from pymongo import ASCENDING, DESCENDING

logger = logging.getLogger(__name__)


class DBWrapper:
    """Class to represent database wrapper."""

    reference_date: Optional[str] = None

    def __init__(
        self,
        url: str,
        db_name: str,
        collection_name: str,
        tls_cert_key_path: Optional[str] = None,
        tls_ca_path: Optional[str] = None,
    ) -> None:
        """
        Construct DBWrapper instance.

        :param url: connection url string.
        :param db_name: database name.
        :param collection_name: collection name.
        :param tls_cert_key_path: path to certificate key.
        :param tls_ca_path: path to CA certificate.
        """
        tls: Dict[str, Union[str, bool, None]] = {}
        if bool(tls_cert_key_path):
            tls["tls"] = True
            tls["tlsCertificateKeyFile"] = tls_cert_key_path
            if bool(tls_ca_path):
                tls["tlsCAFile"] = tls_ca_path

        self.client: AgnosticClient = AsyncIOMotorClient(
            url, connectTimeoutMS=1000, retryWrites=True, **tls
        )
        self.db: AsyncIOMotorDatabase = self.client[db_name]
        self.collection: AsyncIOMotorCollection = self.db[collection_name]
        self.is_closed = False

    def close(self) -> None:
        """Close database connection."""
        self.client.close()
        self.is_closed = True

    async def drop_collection(self, collection_name: str) -> None:
        """
        Drop collection by name.

        :param collection_name: collection name.
        :return: None
        """
        await self.db[collection_name].drop()

    async def get_reference_date(self) -> Optional[str]:
        """
        Return last date from database.

        :return: last date as string.
        """
        if not self.reference_date:
            result = await self.collection.find_one(
                filter={},
                projection={"_id": 0, "date": 1},
                sort=[("date", DESCENDING)],
            )
            if result:
                self.reference_date = result.get("date")
        return self.reference_date

    async def get_districts(self) -> List[str]:
        """
        Return list of districts.

        :return: list of districts.
        """
        reference_date = await self.get_reference_date()
        if reference_date:
            return cast(
                List[str],
                await self.collection.distinct(
                    "district", filter={"date": reference_date}
                ),
            )
        else:
            logger.error("Failed to get reference date.")
            return []

    async def get_localities(self, district_name: str) -> List[str]:
        """
        Return list of district localities.

        :param district_name: district name.
        :return: list of localities.
        """
        reference_date = await self.get_reference_date()
        if reference_date:
            return cast(
                List[str],
                await self.collection.distinct(
                    "localities.locality",
                    filter={"date": reference_date, "district": district_name},
                ),
            )
        else:
            logger.error("Failed to get reference date.")
            return []

    async def get_district(
        self, district_name: str
    ) -> List[Dict[str, Union[str, int, float]]]:
        """
        Return data by district name.

        :param district_name: district name.
        :return:
        """
        return cast(
            List[Dict[str, Union[str, int, float]]],
            await self.collection.find(
                filter={"district": district_name},
                projection={"_id": 0, "localities": 0},
                sort=("date",),
            ),
        )

    async def get_locality(self, district_name: str, locality_name: str) -> List[str]:
        """
        Return locality data by district and locality names.

        :param district_name: district name.
        :param locality_name: locality name.
        :return: list of districts localities.
        """
        filter_ = {
            "district": district_name,
            "localities.locality": locality_name,
        }
        list_length = await self.collection.count_documents(filter_)
        if list_length:
            return cast(
                List[str],
                await self.collection.find(
                    filter=filter_,
                    projection={
                        "_id": 0,
                        "date": 1,
                        "localities": {"$elemMatch": {"locality": locality_name}},
                    },
                    sort=[("date", ASCENDING)],
                ).to_list(length=list_length),
            )
        else:
            return []


async def close_db(app: web.Application) -> None:
    """
    Close connection with database.

    :param app: application instance.
    :return: None
    """
    db = app["db"]
    db.close()


def init_db(app: web.Application) -> None:
    """
    Initialize database wrapper.

    :param app: application instance.
    :return: None
    """
    db_uri = app["config"]["DB_URI"]
    db_name = app["config"]["DB_NAME"]
    collection_name = app["config"]["DB_COLLECTION_NAME"]
    tls_cert_key_path = app["config"]["TLS_CERT_KEY_PATH"]
    tls_ca_path = app["config"]["TLS_CA_PATH"]

    app["db"] = DBWrapper(
        db_uri, db_name, collection_name, tls_cert_key_path, tls_ca_path
    )

    app.on_cleanup.append(close_db)
