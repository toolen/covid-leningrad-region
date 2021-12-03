from typing import List, Dict, Union

from aiohttp import web
from pymongo import MongoClient
from pymongo.collection import Collection


class DBWrapper:
    client = None
    db_name = None
    collection_name = None
    reference_date = None

    def __init__(self, uri, db_name, collection_name, tls_cert_key_path=None, tls_ca_path=None) -> None:
        tls = {}
        if tls_cert_key_path:
            tls['tls'] = True
            tls['tlsCertificateKeyFile'] = tls_cert_key_path
            if tls_ca_path:
                tls['tlsCAFile'] = tls_ca_path

        self.db_name = db_name
        self.collection_name = collection_name
        self.client = MongoClient(
            uri,
            connectTimeoutMS=1000,
            retryWrites=True,
            **tls
        )

        self.reference_date = self.get_reference_date()

    def get_collection(self) -> Collection:
        return self.client[self.db_name][self.collection_name]

    def close(self):
        self.client.close()

    def get_reference_date(self):
        reference_date = self.get_collection().find_one(
            filter={},
            projection={'_id': 0, 'date': 1},
            sort={'date': -1},
        ).get('date')
        if reference_date:
            return reference_date
        else:
            raise Exception()

    def get_districts(self) -> List[str]:
        collection = self.get_collection()
        return collection.distinct('district', filter={'date': self.reference_date}, sort=('district',))
        # return list(map(lambda x: x.get('district'), collection.find(
        #     filter={'date': yesterday},
        #     projection={'_id': 0, 'district': 1},
        #     sort=('district',),
        # )))

    def get_localities(self, district_name):
        collection = self.get_collection()
        return collection.distinct(
            'localities.locality',
            filter={'date': self.reference_date, 'district': district_name},
            sort=('localities.locality',)
        )
        # return collection.find(
        #     filter={'district': district_name},
        #     projection={'_id': 0, 'localities.locality': 1},
        #     sort=('date',),
        # )

    def get_district(self, district_name: str) -> List[Dict[str, Union[str, int, float]]]:
        collection = self.get_collection()
        return collection.find(
            filter={'district': district_name},
            projection={'_id': 0, 'localities': 0},
            sort=('date',),
        )

    def get_locality(self, district_name: str, locality_name: str):
        collection = self.get_collection()
        return collection.find(
            filter={'district': district_name, 'localities.locality': locality_name},
            projection={'date': 1, 'localities': {"$elemMatch": {'locality': 'г. Бокситогорск'}}},
            sort=('date',),
        )


async def close_db(app: web.Application) -> None:
    db = app['db']
    db.close()


def init_db(app: web.Application) -> None:
    db_uri = app['config']['DB_URI']
    db_name = app['config']['DB_NAME']
    collection_name = app['config']['DB_COLLECTION_NAME']
    tls_cert_key_path = app['config']['TLS_CERT_KEY_PATH']
    tls_ca_path = app['config']['TLS_CA_PATH']

    app['db'] = DBWrapper(db_uri, db_name, collection_name, tls_cert_key_path, tls_ca_path)

    app.on_cleanup.append(close_db)
