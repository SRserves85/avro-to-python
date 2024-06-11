# -*- coding: utf-8 -*-

""" avro python class for file: RecordWithArrayOfMap """

import json
from helpers import default_json_serialize, default_json_deserialize, todict, is_assignable
from typing import Union


class RecordWithArrayOfMap(object):

    schema = """
    {
        "type": "record",
        "name": "RecordWithArrayOfMap",
        "namespace": "records",
        "fields": [
            {
                "name": "things",
                "type": {
                    "type": "array",
                    "items": {
                        "type": "map",
                        "values": "string"
                    }
                },
                "default": []
            }
        ]
    }
    """

    def __init__(self, obj: Union[str, dict, 'RecordWithArrayOfMap'] = None) -> None:
        if obj is None:
            return

        if isinstance(obj, str):
            obj = json.loads(obj)

        elif isinstance(obj, type(self)):
            obj = obj.__dict__

        elif not isinstance(obj, dict):
            raise TypeError(
                f"{type(obj)} is not in ('str', 'dict', 'RecordWithArrayOfMap')"
            )

        self.set_things(obj.get('things', None))

    def dict(self):
        return todict(self)

    def set_things(self, values: list) -> None:
        self.things = []
        if isinstance(values, list):
            for element in values:
                self.things.append(element)
        else:
            raise TypeError(f"Field 'things' should be type list but was: {values}")

    def get_things(self) -> list:
        return self.things

    def serialize(self) -> None:
        return json.dumps(self, default=default_json_serialize)
