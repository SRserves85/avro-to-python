# -*- coding: utf-8 -*-

""" avro python class for file: RecordWithNestedMap """

import json
from helpers import default_json_serialize, default_json_deserialize, todict, is_assignable
from typing import Union
from records.Thing import Thing


class RecordWithNestedMap(object):

    schema = """
    {
        "type": "record",
        "name": "RecordWithNestedMap",
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
                "name": "nestedThingMap",
                "type": {
                    "type": "map",
                    "values": {
                        "type": "map",
                        "values": "Thing"
                    }
                }
            },
            {
                "name": "nestedIntMap",
                "type": {
                    "type": "map",
                    "values": {
                        "type": "map",
                        "values": "int"
                    }
                }
            },
            {
                "name": "mappedThingArray",
                "type": {
                    "type": "map",
                    "values": {
                        "type": "array",
                        "items": {
                            "type": "Thing"
                        }
                    }
                }
            }
        ]
    }
    """

    def __init__(self, obj: Union[str, dict, 'RecordWithNestedMap'] = None) -> None:
        if obj is None:
            return

        if isinstance(obj, str):
            obj = json.loads(obj)

        elif isinstance(obj, type(self)):
            obj = obj.__dict__

        elif not isinstance(obj, dict):
            raise TypeError(
                f"{type(obj)} is not in ('str', 'dict', 'RecordWithNestedMap')"
            )

        self.set_thingMap(obj.get('thingMap', None))

        self.set_nestedThingMap(obj.get('nestedThingMap', None))

        self.set_nestedIntMap(obj.get('nestedIntMap', None))

        self.set_mappedThingArray(obj.get('mappedThingArray', None))

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

    def set_nestedThingMap(self, values: list) -> None:

        self.nestedThingMap = []
        if isinstance(values, list):
            for item in values:
                for key, value in item.items():

                    if not isinstance(key, str):
                        raise TypeError(
                            "Keys in map types must be strings!"
                        )
                    sub_array = []
                    if isinstance(value, list):
                        for sub_item in value:
                            for sub_key, sub_value in sub_item.items():
                                if not isinstance(sub_key, str):
                                    raise TypeError(
                                        "keys in map types must be strings"
                                    )
                                sub_array.append({sub_key: Thing(sub_value)})
                    self.nestedThingMap.append({key: sub_array})
        else:
            raise TypeError(f"Field 'nestedThingMap' should be type list but was: {values}")

    def get_nestedThingMap(self) -> list:
        return self.nestedThingMap

    def set_nestedIntMap(self, values: list) -> None:

        self.nestedIntMap = []
        if isinstance(values, list):
            for item in values:
                for key, value in item.items():

                    if not isinstance(key, str):
                        raise TypeError(
                            "Keys in map types must be strings!"
                        )
                    sub_array = []
                    if isinstance(value, list):
                        for sub_item in value:
                            for sub_key, sub_value in sub_item.items():
                                if not isinstance(sub_key, str):
                                    raise TypeError(
                                        "keys in map types must be strings"
                                    )
                                if isinstance(sub_value, int):
                                    sub_array.append({sub_key: sub_value})
                                else:
                                    raise TypeError(
                                        f"Type for 'nestedIntMap' should be 'int' but was: {sub_value}"
                                    )
                    self.nestedIntMap.append({key: sub_array})
        else:
            raise TypeError(f"Field 'nestedIntMap' should be type list but was: {values}")

    def get_nestedIntMap(self) -> list:
        return self.nestedIntMap

    def set_mappedThingArray(self, values: list) -> None:

        self.mappedThingArray = []
        if isinstance(values, list):
            for item in values:
                for key, value in item.items():

                    if not isinstance(key, str):
                        raise TypeError(
                            "Keys in map types must be strings!"
                        )
                    sub_array = []
                    if isinstance(value, list):
                        for element in value:
                            sub_array.append(Thing(element))
        else:
            raise TypeError(f"Field 'mappedThingArray' should be type list but was: {values}")

    def get_mappedThingArray(self) -> list:
        return self.mappedThingArray

    def serialize(self) -> None:
        return json.dumps(self, default=default_json_serialize)
