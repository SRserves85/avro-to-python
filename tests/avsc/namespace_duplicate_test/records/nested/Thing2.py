# -*- coding: utf-8 -*-

""" avro python class for file: Thing2 """

import json
from helpers import default_json_serialize, default_json_deserialize, todict, is_assignable
from typing import Union


class Thing2(object):

    schema = """
    {
        "type": "record",
        "name": "Thing2",
        "namespace": "records.nested",
        "fields": [
            {
                "name": "chars",
                "type": "string"
            }
        ]
    }
    """

    def __init__(self, obj: Union[str, dict, 'Thing2'] = None) -> None:
        if obj is None:
            return

        if isinstance(obj, str):
            obj = json.loads(obj)

        elif isinstance(obj, type(self)):
            obj = obj.__dict__

        elif not isinstance(obj, dict):
            raise TypeError(
                f"{type(obj)} is not in ('str', 'dict', 'Thing2')"
            )

        self.set_chars(default_json_deserialize(obj.get('chars', None), str))

    def dict(self):
        return todict(self)

    def set_chars(self, value: str) -> None:
        if isinstance(value, str):
            self.chars = value
        else:
            raise TypeError(f"field 'chars' should be type str but was: {value}")

    def get_chars(self) -> str:
        return self.chars

    def serialize(self) -> None:
        return json.dumps(self, default=default_json_serialize)
