# -*- coding: utf-8 -*-

""" avro python class for file: RecordWithRecord """

import json
from test_avro.helpers import default_json_serialize, todict
from typing import Union
from test_avro.records.Thing import Thing


class RecordWithRecord(object):

    schema = """
    {
        "type": "record",
        "name": "RecordWithRecord",
        "namespace": "records",
        "fields": [
            {
                "name": "thing1",
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
                "name": "thing2",
                "type": "Thing",
                "default": {
                    "id": 0
                }
            }
        ]
    }
    """

    def __init__(self, obj: Union[str, dict, 'RecordWithRecord']) -> None:
        if isinstance(obj, str):
            obj = json.loads(obj)

        elif isinstance(obj, type(self)):
            obj = obj.__dict__

        elif not isinstance(obj, dict):
            raise TypeError(
                f"{type(obj)} is not in ('str', 'dict', 'RecordWithRecord')"
            )

        self.set_thing1(obj.get('thing1', None))

        self.set_thing2(obj.get('thing2', {'id': 0}))

    def dict(self):
        return todict(self)

    def set_thing1(self, values: Thing) -> None:

        self.thing1 = Thing(values)

    def get_thing1(self) -> Thing:

        return self.thing1

    def set_thing2(self, values: Thing) -> None:

        self.thing2 = Thing(values)

    def get_thing2(self) -> Thing:

        return self.thing2

    def serialize(self) -> None:
        return json.dumps(self, default=default_json_serialize)
