# -*- coding: utf-8 -*-

""" avro python class for file: ComplexRecord """

import json
from test_avro.helpers import default_json_serialize, todict
from typing import Union
from test_avro.records.Thing import Thing
from test_avro.records.nested.Flavor import Flavor


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

    def __init__(self, obj: Union[str, dict, 'ComplexRecord']) -> None:
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
