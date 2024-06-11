# -*- coding: utf-8 -*-

""" avro python class for file: CommonReference """

import json
from helpers import default_json_serialize, default_json_deserialize, todict, is_assignable
from typing import Union


class CommonReference(object):

    schema = """
    {
        "type": "record",
        "name": "CommonReference",
        "fields": [
            {
                "name": "group",
                "type": "int"
            },
            {
                "name": "isApproved",
                "type": [
                    "null",
                    "boolean"
                ],
                "default": null
            },
            {
                "name": "index",
                "type": [
                    "null",
                    "int"
                ]
            }
        ],
        "namespace": "records.nested"
    }
    """

    def __init__(self, obj: Union[str, dict, 'CommonReference'] = None) -> None:
        if obj is None:
            return

        if isinstance(obj, str):
            obj = json.loads(obj)

        elif isinstance(obj, type(self)):
            obj = obj.__dict__

        elif not isinstance(obj, dict):
            raise TypeError(
                f"{type(obj)} is not in ('str', 'dict', 'CommonReference')"
            )

        self.set_group(default_json_deserialize(obj.get('group', None), int))

        self.set_isApproved(default_json_deserialize(obj.get('isApproved', None), bool))

        self.set_index(default_json_deserialize(obj.get('index', None), int))

    def dict(self):
        return todict(self)

    def set_group(self, value: int) -> None:
        if isinstance(value, int):
            self.group = value
        else:
            raise TypeError(f"field 'group' should be type int but was: {value}")

    def get_group(self) -> int:
        return self.group

    def set_isApproved(self, value: Union[None, bool]) -> None:
        if value is None:
            self.isApproved = None

        elif isinstance(value, bool):
            self.isApproved = bool(value)
        else:
            raise TypeError(f"field 'isApproved' should be in (None, bool) but was: {value}")

    def get_isApproved(self) -> Union[None, bool]:
        return self.isApproved

    def set_index(self, value: Union[None, int]) -> None:
        if value is None:
            self.index = None

        elif isinstance(value, int):
            self.index = int(value)
        else:
            raise TypeError(f"field 'index' should be in (None, int) but was: {value}")

    def get_index(self) -> Union[None, int]:
        return self.index

    def serialize(self) -> None:
        return json.dumps(self, default=default_json_serialize)
