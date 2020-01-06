# -*- coding: utf-8 -*-

""" avro python class for file: ExampleEvent """

import json
from test_avro.helpers import default_json_serialize, todict
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

    def __init__(self, obj: Union[str, dict, 'ExampleEvent']) -> None:
        if isinstance(obj, str):
            obj = json.loads(obj)

        elif isinstance(obj, type(self)):
            obj = obj.__dict__

        elif not isinstance(obj, dict):
            raise TypeError(
                f"{type(obj)} is not in ('str', 'dict', 'ExampleEvent')"
            )

        self.set_name(obj.get('name', None))

        self.set_active(obj.get('active', True))

        self.set_salary(obj.get('salary', None))

    def dict(self):
        return todict(self)

    def set_name(self, value: str) -> None:

        if isinstance(value, str):
            self.name = value
        else:
            raise TypeError("field 'name' should be type str")

    def get_name(self) -> str:

        return self.name

    def set_active(self, value: bool) -> None:

        if isinstance(value, bool):
            self.active = value
        else:
            raise TypeError("field 'active' should be type bool")

    def get_active(self) -> bool:

        return self.active

    def set_salary(self, value: int) -> None:

        if isinstance(value, int):
            self.salary = value
        else:
            raise TypeError("field 'salary' should be type int")

    def get_salary(self) -> int:

        return self.salary

    def serialize(self) -> None:
        return json.dumps(self, default=default_json_serialize)
