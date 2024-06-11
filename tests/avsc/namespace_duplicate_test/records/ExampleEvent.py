# -*- coding: utf-8 -*-

""" avro python class for file: ExampleEvent """

import json
from helpers import default_json_serialize, default_json_deserialize, todict, is_assignable
from typing import Union


class ExampleEvent(object):

    schema = """
    {
        "type": "record",
        "name": "ExampleEvent",
        "namespace": "records",
        "doc": "This is an example schema.",
        "fields": [
            {
                "name": "name",
                "type": "string"
            },
            {
                "name": "active",
                "type": "boolean",
                "default": true
            },
            {
                "name": "salary",
                "type": "long"
            }
        ]
    }
    """

    def __init__(self, obj: Union[str, dict, 'ExampleEvent'] = None) -> None:
        if obj is None:
            return

        if isinstance(obj, str):
            obj = json.loads(obj)

        elif isinstance(obj, type(self)):
            obj = obj.__dict__

        elif not isinstance(obj, dict):
            raise TypeError(
                f"{type(obj)} is not in ('str', 'dict', 'ExampleEvent')"
            )

        self.set_name(default_json_deserialize(obj.get('name', None), str))

        self.set_active(default_json_deserialize(obj.get('active', True), bool))

        self.set_salary(default_json_deserialize(obj.get('salary', None), int))

    def dict(self):
        return todict(self)

    def set_name(self, value: str) -> None:
        if isinstance(value, str):
            self.name = value
        else:
            raise TypeError(f"field 'name' should be type str but was: {value}")

    def get_name(self) -> str:
        return self.name

    def set_active(self, value: bool) -> None:
        if isinstance(value, bool):
            self.active = value
        else:
            raise TypeError(f"field 'active' should be type bool but was: {value}")

    def get_active(self) -> bool:
        return self.active

    def set_salary(self, value: int) -> None:
        if isinstance(value, int):
            self.salary = value
        else:
            raise TypeError(f"field 'salary' should be type int but was: {value}")

    def get_salary(self) -> int:
        return self.salary

    def serialize(self) -> None:
        return json.dumps(self, default=default_json_serialize)
