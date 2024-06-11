# -*- coding: utf-8 -*-

""" avro python class for file: ComplexRecord """

import json
from helpers import default_json_serialize, default_json_deserialize, todict, is_assignable
from typing import Union
from records.Thing import Thing
from records.nested.Flavor import Flavor


class ComplexRecord(object):

    schema = """
    {
        "type": "record",
        "name": "ComplexRecord",
        "namespace": "records",
        "fields": [
            {
                "name": "thing",
                "type": {
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
            },
            {
                "name": "flavor",
                "type": {
                    "type": "enum",
                    "name": "Flavor",
                    "namespace": "records.nested",
                    "symbols": [
                        "VANILLA",
                        "CHOCOLATE",
                        "STRAWBERRY"
                    ]
                }
            }
        ]
    }
    """

    def __init__(self, obj: Union[str, dict, 'ComplexRecord'] = None) -> None:
        if obj is None:
            return

        if isinstance(obj, str):
            obj = json.loads(obj)

        elif isinstance(obj, type(self)):
            obj = obj.__dict__

        elif not isinstance(obj, dict):
            raise TypeError(
                f"{type(obj)} is not in ('str', 'dict', 'ComplexRecord')"
            )

        self.set_thing(obj.get('thing', None))

        self.set_flavor(obj.get('flavor', None))

    def dict(self):
        return todict(self)

    def set_thing(self, values: Thing) -> None:

        self.thing = Thing(values)

    def get_thing(self) -> Thing:

        return self.thing

    def set_flavor(self, values: Flavor) -> None:

        self.flavor = Flavor(values)

    def get_flavor(self) -> Flavor:

        return self.flavor

    def serialize(self) -> None:
        return json.dumps(self, default=default_json_serialize)
