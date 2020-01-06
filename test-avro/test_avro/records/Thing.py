# -*- coding: utf-8 -*-

""" avro python class for file: Thing """

import json
from test_avro.helpers import default_json_serialize, todict
from typing import Union


class Thing(object):

    schema = """
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
    """

    def __init__(self, obj: Union[str, dict, 'Thing']) -> None:
        if isinstance(obj, str):
            obj = json.loads(obj)

        elif isinstance(obj, type(self)):
            obj = obj.__dict__

        elif not isinstance(obj, dict):
            raise TypeError(
                f"{type(obj)} is not in ('str', 'dict', 'Thing')"
            )

        self.set_id(obj.get('id', None))

    def dict(self):
        return todict(self)

    def set_id(self, value: int) -> None:

        if isinstance(value, int):
            self.id = value
        else:
            raise TypeError("field 'id' should be type int")

    def get_id(self) -> int:

        return self.id

    def serialize(self) -> None:
        return json.dumps(self, default=default_json_serialize)
