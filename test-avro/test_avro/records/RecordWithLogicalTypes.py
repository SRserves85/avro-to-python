# -*- coding: utf-8 -*-

""" avro python class for file: RecordWithLogicalTypes """

import json
from test_avro.helpers import default_json_serialize, todict
from typing import Union


class RecordWithLogicalTypes(object):

    schema = """
    {
        "type": "record",
        "name": "RecordWithLogicalTypes",
        "namespace": "records",
        "fields": [
            {
                "name": "timestamp",
                "type": {
                    "type": "long",
                    "logicalType": "timestamp-millis"
                }
            }
        ]
    }
    """

    def __init__(self, obj: Union[str, dict, 'RecordWithLogicalTypes']) -> None:
        if isinstance(obj, str):
            obj = json.loads(obj)

        elif isinstance(obj, type(self)):
            obj = obj.__dict__

        elif not isinstance(obj, dict):
            raise TypeError(
                f"{type(obj)} is not in ('str', 'dict', 'RecordWithLogicalTypes')"
            )

        self.set_timestamp(obj.get('timestamp', None))

    def dict(self):
        return todict(self)

    def set_timestamp(self, value: int) -> None:

        if isinstance(value, int):
            self.timestamp = value
        else:
            raise TypeError("field 'timestamp' should be type int")

    def get_timestamp(self) -> int:

        return self.timestamp

    def serialize(self) -> None:
        return json.dumps(self, default=default_json_serialize)
