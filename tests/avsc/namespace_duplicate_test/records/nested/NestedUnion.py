# -*- coding: utf-8 -*-

""" avro python class for file: NestedUnion """

import json
from helpers import default_json_serialize, default_json_deserialize, todict, is_assignable
from typing import Union
from records.nested.CommonReference import CommonReference


class NestedUnion(object):

    schema = """
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
    """

    def __init__(self, obj: Union[str, dict, 'NestedUnion'] = None) -> None:
        if obj is None:
            return

        if isinstance(obj, str):
            obj = json.loads(obj)

        elif isinstance(obj, type(self)):
            obj = obj.__dict__

        elif not isinstance(obj, dict):
            raise TypeError(
                f"{type(obj)} is not in ('str', 'dict', 'NestedUnion')"
            )

        self.set_categories(obj.get('categories', None))

    def dict(self):
        return todict(self)

    def set_categories(self, value: Union[None, list]) -> None:
        if value is None:
            self.categories = None

        elif isinstance(value, list):
            self.categories = []
            for element in value:
                self.categories.append(CommonReference(element))
        else:
            raise TypeError(f"field 'categories' should be in (None, list) but was: {value}")

    def get_categories(self) -> Union[None, list]:
        return self.categories

    def serialize(self) -> None:
        return json.dumps(self, default=default_json_serialize)
