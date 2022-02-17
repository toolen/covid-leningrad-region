import pytest

from dashboard_backend.config import get_config
from dashboard_backend.db import DBWrapper


@pytest.fixture
async def db():
    config = get_config()
    collection_name = f"{config['DB_NAME']}_test"
    db = DBWrapper(
        config["DB_URI"],
        collection_name,
        config["DB_COLLECTION_NAME"],
        config["TLS_CERT_KEY_PATH"],
        config["TLS_CA_PATH"],
    )
    yield db
    await db.drop_collection(collection_name)
    db.close()
