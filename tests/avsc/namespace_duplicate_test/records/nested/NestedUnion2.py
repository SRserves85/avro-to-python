# -*- coding: utf-8 -*-

""" avro python class for file: NestedUnion2 """

import json
from helpers import default_json_serialize, default_json_deserialize, todict, is_assignable
from typing import Union
from records.nested.CommonReference import CommonReference


class NestedUnion2(object):

    schema = """
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
    """

    def __init__(self, obj: Union[str, dict, 'NestedUnion2'] = None) -> None:
        if obj is None:
            return

        if isinstance(obj, str):
            obj = json.loads(obj)

        elif isinstance(obj, type(self)):
            obj = obj.__dict__

        elif not isinstance(obj, dict):
            raise TypeError(
                f"{type(obj)} is not in ('str', 'dict', 'NestedUnion2')"
            )

        self.set_categories2(obj.get('categories2', None))

    def dict(self):
        return todict(self)

    def set_categories2(self, value: Union[None, list]) -> None:
        if value is None:
            self.categories2 = None

        elif isinstance(value, list):
            self.categories2 = []
            for element in value:
                self.categories2.append(CommonReference(element))
        else:
            raise TypeError(f"field 'categories2' should be in (None, list) but was: {value}")

    def get_categories2(self) -> Union[None, list]:
        return self.categories2

    def serialize(self) -> None:
        return json.dumps(self, default=default_json_serialize)
