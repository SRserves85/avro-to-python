# -*- coding: utf-8 -*-

""" avro python class for file: RecordWithNestedUnion """

import json
from helpers import default_json_serialize, default_json_deserialize, todict, is_assignable
from typing import Union
from records.nested.NestedUnion import NestedUnion
from records.nested.NestedUnion2 import NestedUnion2


class RecordWithNestedUnion(object):

    schema = """
    {
        "type": "record",
        "name": "RecordWithNestedUnion",
        "namespace": "records",
        "fields": [
            {
                "name": "nestedUnion",
                "type": [
                    "null",
                    {
                        "type": "record",
                        "name": "NestedUnion",
                        "namespace": "records.nested",
                        "fields": [
                            {
                                "name": "categories",
                                "type": [
                                    "null",
                                    {
                                        "type": "array",
                                        "items": {
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
                                    }
                                ],
                                "default": null
                            }
                        ]
                    }
                ],
                "default": null
            },
            {
                "name": "nestedUnion2",
                "type": [
                    "null",
                    {
                        "type": "record",
                        "name": "NestedUnion2",
                        "namespace": "records.nested",
                        "fields": [
                            {
                                "name": "categories2",
                                "type": [
                                    "null",
                                    {
                                        "type": "array",
                                        "items": {
                                            "type": "CommonReference"
                                        }
                                    }
                                ],
                                "default": null
                            }
                        ]
                    }
                ],
                "default": null
            }
        ]
    }
    """

    def __init__(self, obj: Union[str, dict, 'RecordWithNestedUnion'] = None) -> None:
        if obj is None:
            return

        if isinstance(obj, str):
            obj = json.loads(obj)

        elif isinstance(obj, type(self)):
            obj = obj.__dict__

        elif not isinstance(obj, dict):
            raise TypeError(
                f"{type(obj)} is not in ('str', 'dict', 'RecordWithNestedUnion')"
            )

        self.set_nestedUnion(obj.get('nestedUnion', None))

        self.set_nestedUnion2(obj.get('nestedUnion2', None))

    def dict(self):
        return todict(self)

    def set_nestedUnion(self, value: Union[None, NestedUnion]) -> None:
        if value is None:
            self.nestedUnion = None

        elif is_assignable(value, NestedUnion):
            self.nestedUnion = NestedUnion(value)
        else:
            raise TypeError(f"field 'nestedUnion' should be in (None, NestedUnion) but was: {value}")

    def get_nestedUnion(self) -> Union[None, NestedUnion]:
        return self.nestedUnion

    def set_nestedUnion2(self, value: Union[None, NestedUnion2]) -> None:
        if value is None:
            self.nestedUnion2 = None

        elif is_assignable(value, NestedUnion2):
            self.nestedUnion2 = NestedUnion2(value)
        else:
            raise TypeError(f"field 'nestedUnion2' should be in (None, NestedUnion2) but was: {value}")

    def get_nestedUnion2(self) -> Union[None, NestedUnion2]:
        return self.nestedUnion2

    def serialize(self) -> None:
        return json.dumps(self, default=default_json_serialize)
