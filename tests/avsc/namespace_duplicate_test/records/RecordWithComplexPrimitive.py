# -*- coding: utf-8 -*-

""" avro python class for file: RecordWithComplexPrimitive """

import json
from helpers import default_json_serialize, todict
from typing import Union


class RecordWithComplexPrimitive(object):

    schema = """
    {
        "type": "record",
        "name": "RecordWithComplexPrimitive",
        "namespace": "records",
        "fields": [
            {
                "name": "binaryData",
                "type": {
                    "type": "bytes",
                    "java-class": "[B"
                }
            }
        ]
    }
    """

    def __init__(self, obj: Union[str, dict, 'RecordWithComplexPrimitive']) -> None:
        if isinstance(obj, str):
            obj = json.loads(obj)

        elif isinstance(obj, type(self)):
            obj = obj.__dict__

        elif not isinstance(obj, dict):
            raise TypeError(
                f"{type(obj)} is not in ('str', 'dict', 'RecordWithComplexPrimitive')"
            )

        self.set_binaryData(obj.get('binaryData', None))

    def dict(self):
        return todict(self)

    def set_binaryData(self, value: bytes) -> None:

        if isinstance(value, bytes):
            self.binaryData = value
        else:
            raise TypeError("field 'binaryData' should be type bytes")

    def get_binaryData(self) -> bytes:

        return self.binaryData

    def serialize(self) -> None:
        return json.dumps(self, default=default_json_serialize)
