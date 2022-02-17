from datetime import datetime, timedelta
from typing import List

from dashboard_backend.db import DBWrapper


async def test_get_districts(db: DBWrapper) -> None:
    date_ = datetime.now()
    await db.collection.insert_many(
        [
            {"district": "one", "date": date_},
            {"district": "two", "date": date_},
            {"district": "three", "date": date_},
            {"district": "four", "date": date_ - timedelta(days=1)},
        ]
    )

    districts = await db.get_districts()

    assert isinstance(districts, List)
    assert len(districts) == 3
    assert "one" in districts
    assert "two" in districts
    assert "three" in districts


async def test_get_localities(db: DBWrapper) -> None:
    date_ = datetime.now()
    await db.collection.insert_one(
        {
            "district": "foo",
            "date": date_,
            "localities": [
                {"locality": "one"},
                {"locality": "two"},
                {"locality": "three"},
            ],
        },
        {
            "district": "bar",
            "date": date_ - timedelta(days=1),
            "localities": [
                {"locality": "one"},
                {"locality": "two"},
                {"locality": "three"},
            ],
        },
    )

    localities = await db.get_localities("foo")

    assert isinstance(localities, List)
    assert len(localities) == 3
    assert "one" in localities
    assert "two" in localities
    assert "three" in localities
