# -*- coding: utf-8 -*-

""" avro python class for file: RecordWithArray """

import json
from test_avro.helpers import default_json_serialize, todict
from typing import Union
from test_avro.records.Thing import Thing


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
                        "type": "int"
                    }
                }
            }
        ]
    }
    """

    def __init__(self, obj: Union[str, dict, 'RecordWithArray']) -> None:
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

    def dict(self):
        return todict(self)

    def set_things(self, values: list) -> None:

        self.things = []
        if isinstance(values, list):
            for element in values:
                self.things.append(Thing(element))
        else:
            raise TypeError("Field 'things' should be type list")

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
                        "Type for 'numbers' should be 'int'"
                    )
        else:
            raise TypeError("Field 'numbers' should be type list")

    def get_numbers(self) -> list:
        return self.numbers

    def serialize(self) -> None:
        return json.dumps(self, default=default_json_serialize)
