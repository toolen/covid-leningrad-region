"""This file contains custom JSON encoders."""
import datetime
import json
from typing import Any


class MongoEncoder(json.JSONEncoder):
    """This encoder supports datetime."""

    def default(self, o: Any) -> Any:
        """
        Convert to JSON value.

        :param o: any object.
        :return: serialized object.
        """
        if isinstance(o, datetime.datetime):
            return o.isoformat()
            # return o.timestamp()
        return super().default(o)


def mongo_dumps(data: Any) -> str:
    """
    Serialize ``obj`` to a JSON formatted ``str``.

    :param data: data to serialize.
    :return: serialized data.
    """
    return json.dumps(data, cls=MongoEncoder)
