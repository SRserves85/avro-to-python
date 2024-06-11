# -*- coding: utf-8 -*-

""" avro python class for file: RecordWithUnion """

import json
from helpers import default_json_serialize, default_json_deserialize, todict, is_assignable
from typing import Union
from records.Thing import Thing
from records.nested.Flavor import Flavor


class RecordWithUnion(object):

    schema = """
    {
        "type": "record",
        "name": "RecordWithUnion",
        "namespace": "records",
        "fields": [
            {
                "name": "optionalString",
                "type": [
                    "string",
                    "null"
                ]
            },
            {
                "name": "intOrThing",
                "type": [
                    "int",
                    {
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
                ]
            },
            {
                "name": "nullOrThingArray",
                "type": [
                    "null",
                    {
                        "type": "array",
                        "items": {
                            "type": "Thing"
                        }
                    }
                ]
            },
            {
                "name": "nullOrMap",
                "type": [
                    "null",
                    {
                        "type": "map",
                        "values": "float"
                    }
                ]
            },
            {
                "name": "nullOrEnum",
                "type": [
                    "null",
                    {
                        "type": "enum",
                        "name": "Flavor",
                        "namespace": "records.nested",
                        "symbols": [
                            "VANILLA",
                            "CHOCOLATE",
                            "STRAWBERRY"
                        ]
                    }
                ]
            }
        ]
    }
    """

    def __init__(self, obj: Union[str, dict, 'RecordWithUnion'] = None) -> None:
        if obj is None:
            return

        if isinstance(obj, str):
            obj = json.loads(obj)

        elif isinstance(obj, type(self)):
            obj = obj.__dict__

        elif not isinstance(obj, dict):
            raise TypeError(
                f"{type(obj)} is not in ('str', 'dict', 'RecordWithUnion')"
            )

        self.set_optionalString(default_json_deserialize(obj.get('optionalString', None), str))

        self.set_intOrThing(default_json_deserialize(obj.get('intOrThing', None), int))

        self.set_nullOrThingArray(obj.get('nullOrThingArray', None))

        self.set_nullOrMap(obj.get('nullOrMap', None))

        self.set_nullOrEnum(obj.get('nullOrEnum', None))

    def dict(self):
        return todict(self)

    def set_optionalString(self, value: Union[str, None]) -> None:
        if isinstance(value, str):
            self.optionalString = str(value)

        elif value is None:
            self.optionalString = None
        else:
            raise TypeError(f"field 'optionalString' should be in (str, None) but was: {value}")

    def get_optionalString(self) -> Union[str, None]:
        return self.optionalString

    def set_intOrThing(self, value: Union[int, Thing]) -> None:
        if isinstance(value, int):
            self.intOrThing = int(value)

        elif is_assignable(value, Thing):
            self.intOrThing = Thing(value)
        else:
            raise TypeError(f"field 'intOrThing' should be in (int, Thing) but was: {value}")

    def get_intOrThing(self) -> Union[int, Thing]:
        return self.intOrThing

    def set_nullOrThingArray(self, value: Union[None, list]) -> None:
        if value is None:
            self.nullOrThingArray = None

        elif isinstance(value, list):
            self.nullOrThingArray = []
            for element in value:
                self.nullOrThingArray.append(Thing(element))
        else:
            raise TypeError(f"field 'nullOrThingArray' should be in (None, list) but was: {value}")

    def get_nullOrThingArray(self) -> Union[None, list]:
        return self.nullOrThingArray

    def set_nullOrMap(self, value: Union[None, dict]) -> None:
        if value is None:
            self.nullOrMap = None

        elif is_assignable(value, dict):
            self.nullOrMap = dict(value)
        else:
            raise TypeError(f"field 'nullOrMap' should be in (None, dict) but was: {value}")

    def get_nullOrMap(self) -> Union[None, dict]:
        return self.nullOrMap

    def set_nullOrEnum(self, value: Union[None, Flavor]) -> None:
        if value is None:
            self.nullOrEnum = None

        elif isinstance(value, (str, Flavor)):
            self.nullOrEnum = Flavor(value)
        else:
            raise TypeError(f"field 'nullOrEnum' should be in (None, Flavor) but was: {value}")

    def get_nullOrEnum(self) -> Union[None, Flavor]:
        return self.nullOrEnum

    def serialize(self) -> None:
        return json.dumps(self, default=default_json_serialize)
