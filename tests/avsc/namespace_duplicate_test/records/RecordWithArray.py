# -*- coding: utf-8 -*-

""" avro python class for file: RecordWithArray """

import json
from helpers import default_json_serialize, default_json_deserialize, todict, is_assignable
from typing import Union
from records.Thing import Thing


class RecordWithArray(object):

    schema = """
    {
        "type": "record",
        "name": "RecordWithArray",
        "namespace": "records",
        "fields": [
            {
                "name": "things",
                "type": {
                    "type": "array",
                    "items": {
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
                "name": "numbers",
                "type": {
                    "type": "array",
                    "items": {
                        "type": "int",
                        "name": null
                    }
                }
            },
            {
                "name": "things2",
                "type": {
                    "type": "array",
                    "items": {
                        "type": "Thing"
                    }
                }
            },
            {
                "name": "twoDimDoubleArray",
                "type": {
                    "type": "array",
                    "items": {
                        "type": "array",
                        "items": {
                            "type": "double",
                            "name": null
                        },
                        "java-class": "[D"
                    },
                    "java-class": "[[D"
                }
            },
            {
                "name": "threeDimRecordArray",
                "type": {
                    "type": "array",
                    "items": {
                        "type": "array",
                        "items": {
                            "type": "array",
                            "items": {
                                "type": "Thing"
                            }
                        }
                    }
                }
            },
            {
                "name": "arrayOfUnion",
                "type": {
                    "type": "array",
                    "items": [
                        "Thing",
                        "int"
                    ]
                }
            }
        ]
    }
    """

    def __init__(self, obj: Union[str, dict, 'RecordWithArray'] = None) -> None:
        if obj is None:
            return

        if isinstance(obj, str):
            obj = json.loads(obj)

        elif isinstance(obj, type(self)):
            obj = obj.__dict__

        elif not isinstance(obj, dict):
            raise TypeError(
                f"{type(obj)} is not in ('str', 'dict', 'RecordWithArray')"
            )

        self.set_things(obj.get('things', None))

        self.set_numbers(obj.get('numbers', None))

        self.set_things2(obj.get('things2', None))

        self.set_twoDimDoubleArray(obj.get('twoDimDoubleArray', None))

        self.set_threeDimRecordArray(obj.get('threeDimRecordArray', None))

        self.set_arrayOfUnion(obj.get('arrayOfUnion', None))

    def dict(self):
        return todict(self)

    def set_things(self, values: list) -> None:
        self.things = []
        if isinstance(values, list):
            for element in values:
                self.things.append(Thing(element))
        else:
            raise TypeError(f"Field 'things' should be type list but was: {values}")

    def get_things(self) -> list:
        return self.things

    def set_numbers(self, values: list) -> None:
        self.numbers = []
        if isinstance(values, list):
            for element in values:
                if isinstance(element, int):
                    self.numbers.append(element)
                else:
                    raise TypeError(
                        f"Type for 'numbers' should be 'int' but was: {element}"
                    )
        else:
            raise TypeError(f"Field 'numbers' should be type list but was: {values}")

    def get_numbers(self) -> list:
        return self.numbers

    def set_things2(self, values: list) -> None:
        self.things2 = []
        if isinstance(values, list):
            for element in values:
                self.things2.append(Thing(element))
        else:
            raise TypeError(f"Field 'things2' should be type list but was: {values}")

    def get_things2(self) -> list:
        return self.things2

    def set_twoDimDoubleArray(self, values: list) -> None:
        self.twoDimDoubleArray = []
        if isinstance(values, list):
            for element in values:
                self.twoDimDoubleArray.append(element)
        else:
            raise TypeError(f"Field 'twoDimDoubleArray' should be type list but was: {values}")

    def get_twoDimDoubleArray(self) -> list:
        return self.twoDimDoubleArray

    def set_threeDimRecordArray(self, values: list) -> None:
        self.threeDimRecordArray = []
        if isinstance(values, list):
            for element in values:
                self.threeDimRecordArray.append(element)
        else:
            raise TypeError(f"Field 'threeDimRecordArray' should be type list but was: {values}")

    def get_threeDimRecordArray(self) -> list:
        return self.threeDimRecordArray

    def set_arrayOfUnion(self, values: list) -> None:
        self.arrayOfUnion = []
        if isinstance(values, list):
            for element in values:
                if is_assignable(element, Thing):
                    self.arrayOfUnion.append(Thing(element))
                
                elif isinstance(element, int):
                    self.arrayOfUnion.append(int(element))
        else:
            raise TypeError(f"Field 'arrayOfUnion' should be type list but was: {values}")

    def get_arrayOfUnion(self) -> list:
        return self.arrayOfUnion

    def serialize(self) -> None:
        return json.dumps(self, default=default_json_serialize)
