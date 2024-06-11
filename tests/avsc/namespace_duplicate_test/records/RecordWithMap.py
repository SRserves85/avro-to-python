# -*- coding: utf-8 -*-

""" avro python class for file: RecordWithMap """

import json
from helpers import default_json_serialize, default_json_deserialize, todict, is_assignable
from typing import Union
from records.Thing import Thing


class RecordWithMap(object):

    schema = """
    {
        "type": "record",
        "name": "RecordWithMap",
        "namespace": "records",
        "fields": [
            {
                "name": "thingMap",
                "type": {
                    "type": "map",
                    "values": {
                        "type": "record",
                        "name": "Thing",
                        "fields": [
                            {
                                "name": "id",
                                "type": "int"
                            }
                        ],
                        "namespace": "records"
                    }
                }
            },
            {
                "name": "intMap",
                "type": {
                    "type": "map",
                    "values": "int"
                }
            },
            {
                "name": "thingMap2",
                "type": {
                    "type": "map",
                    "values": "Thing"
                }
            },
            {
                "name": "thingMap3",
                "type": {
                    "type": "map",
                    "values": "record.Thing"
                }
            }
        ]
    }
    """

    def __init__(self, obj: Union[str, dict, 'RecordWithMap'] = None) -> None:
        if obj is None:
            return

        if isinstance(obj, str):
            obj = json.loads(obj)

        elif isinstance(obj, type(self)):
            obj = obj.__dict__

        elif not isinstance(obj, dict):
            raise TypeError(
                f"{type(obj)} is not in ('str', 'dict', 'RecordWithMap')"
            )

        self.set_thingMap(obj.get('thingMap', None))

        self.set_intMap(obj.get('intMap', None))

        self.set_thingMap2(obj.get('thingMap2', None))

        self.set_thingMap3(obj.get('thingMap3', None))

    def dict(self):
        return todict(self)

    def set_thingMap(self, values: list) -> None:

        self.thingMap = []
        if isinstance(values, list):
            for item in values:
                for key, value in item.items():

                    if not isinstance(key, str):
                        raise TypeError(
                            "Keys in map types must be strings!"
                        )
                    self.thingMap.append({key: Thing(value)})
        else:
            raise TypeError(f"Field 'thingMap' should be type list but was: {values}")

    def get_thingMap(self) -> list:
        return self.thingMap

    def set_intMap(self, values: list) -> None:

        self.intMap = []
        if isinstance(values, list):
            for item in values:
                for key, value in item.items():

                    if not isinstance(key, str):
                        raise TypeError(
                            "Keys in map types must be strings!"
                        )
                    if isinstance(value, int):
                        self.intMap.append({key: value})
                    else:
                        raise TypeError(
                            f"Type for 'intMap' should be 'int' but was: {value}"
                        )
        else:
            raise TypeError(f"Field 'intMap' should be type list but was: {values}")

    def get_intMap(self) -> list:
        return self.intMap

    def set_thingMap2(self, values: list) -> None:

        self.thingMap2 = []
        if isinstance(values, list):
            for item in values:
                for key, value in item.items():

                    if not isinstance(key, str):
                        raise TypeError(
                            "Keys in map types must be strings!"
                        )
                    self.thingMap2.append({key: Thing(value)})
        else:
            raise TypeError(f"Field 'thingMap2' should be type list but was: {values}")

    def get_thingMap2(self) -> list:
        return self.thingMap2

    def set_thingMap3(self, values: list) -> None:

        self.thingMap3 = []
        if isinstance(values, list):
            for item in values:
                for key, value in item.items():

                    if not isinstance(key, str):
                        raise TypeError(
                            "Keys in map types must be strings!"
                        )
                    self.thingMap3.append({key: Thing(value)})
        else:
            raise TypeError(f"Field 'thingMap3' should be type list but was: {values}")

    def get_thingMap3(self) -> list:
        return self.thingMap3

    def serialize(self) -> None:
        return json.dumps(self, default=default_json_serialize)
