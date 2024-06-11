# -*- coding: utf-8 -*-

""" avro python class for file: RecordWithNumbers """

import json
from helpers import default_json_serialize, default_json_deserialize, todict, is_assignable
from typing import Union


class RecordWithNumbers(object):

    schema = """
    {
        "type": "record",
        "name": "RecordWithNumbers",
        "namespace": "records",
        "fields": [
            {
                "name": "booleanValue",
                "type": "boolean"
            },
            {
                "name": "intValue",
                "type": "int"
            },
            {
                "name": "longValue",
                "type": "long"
            },
            {
                "name": "floatValue",
                "type": "float"
            },
            {
                "name": "doubleValue",
                "type": "double"
            }
        ]
    }
    """

    def __init__(self, obj: Union[str, dict, 'RecordWithNumbers'] = None) -> None:
        if obj is None:
            return

        if isinstance(obj, str):
            obj = json.loads(obj)

        elif isinstance(obj, type(self)):
            obj = obj.__dict__

        elif not isinstance(obj, dict):
            raise TypeError(
                f"{type(obj)} is not in ('str', 'dict', 'RecordWithNumbers')"
            )

        self.set_booleanValue(default_json_deserialize(obj.get('booleanValue', None), bool))

        self.set_intValue(default_json_deserialize(obj.get('intValue', None), int))

        self.set_longValue(default_json_deserialize(obj.get('longValue', None), int))

        self.set_floatValue(default_json_deserialize(obj.get('floatValue', None), float))

        self.set_doubleValue(default_json_deserialize(obj.get('doubleValue', None), float))

    def dict(self):
        return todict(self)

    def set_booleanValue(self, value: bool) -> None:
        if isinstance(value, bool):
            self.booleanValue = value
        else:
            raise TypeError(f"field 'booleanValue' should be type bool but was: {value}")

    def get_booleanValue(self) -> bool:
        return self.booleanValue

    def set_intValue(self, value: int) -> None:
        if isinstance(value, int):
            self.intValue = value
        else:
            raise TypeError(f"field 'intValue' should be type int but was: {value}")

    def get_intValue(self) -> int:
        return self.intValue

    def set_longValue(self, value: int) -> None:
        if isinstance(value, int):
            self.longValue = value
        else:
            raise TypeError(f"field 'longValue' should be type int but was: {value}")

    def get_longValue(self) -> int:
        return self.longValue

    def set_floatValue(self, value: float) -> None:
        if isinstance(value, (float, int)):
            self.floatValue = value
        else:
            raise TypeError(f"field 'floatValue' should be type (float, int) but was: {value}")

    def get_floatValue(self) -> float:
        return self.floatValue

    def set_doubleValue(self, value: float) -> None:
        if isinstance(value, (float, int)):
            self.doubleValue = value
        else:
            raise TypeError(f"field 'doubleValue' should be type (float, int) but was: {value}")

    def get_doubleValue(self) -> float:
        return self.doubleValue

    def serialize(self) -> None:
        return json.dumps(self, default=default_json_serialize)
