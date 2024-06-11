# -*- coding: utf-8 -*-

""" avro python class for file: RecordWithBytes """

import json
from helpers import default_json_serialize, default_json_deserialize, todict, is_assignable
from typing import Union


class RecordWithBytes(object):

    schema = """
    {
        "type": "record",
        "name": "RecordWithBytes",
        "namespace": "records",
        "fields": [
            {
                "name": "binaryData",
                "type": "bytes"
            }
        ]
    }
    """

    def __init__(self, obj: Union[str, dict, 'RecordWithBytes'] = None) -> None:
        if obj is None:
            return

        if isinstance(obj, str):
            obj = json.loads(obj)

        elif isinstance(obj, type(self)):
            obj = obj.__dict__

        elif not isinstance(obj, dict):
            raise TypeError(
                f"{type(obj)} is not in ('str', 'dict', 'RecordWithBytes')"
            )

        self.set_binaryData(default_json_deserialize(obj.get('binaryData', None), bytes))

    def dict(self):
        return todict(self)

    def set_binaryData(self, value: bytes) -> None:
        if isinstance(value, bytes):
            self.binaryData = value
        else:
            raise TypeError(f"field 'binaryData' should be type bytes but was: {value}")

    def get_binaryData(self) -> bytes:
        return self.binaryData

    def serialize(self) -> None:
        return json.dumps(self, default=default_json_serialize)
