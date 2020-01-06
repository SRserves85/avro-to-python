# -*- coding: utf-8 -*-

""" avro python class for file: RecordWithEnum """

import json
from test_avro.helpers import default_json_serialize, todict
from typing import Union
from test_avro.records.nested.Flavor import Flavor


class RecordWithEnum(object):

    schema = """
    {
        "type": "record",
        "name": "RecordWithEnum",
        "namespace": "records",
        "fields": [
            {
                "name": "favoriteFlavor",
                "type": {
                    "type": "enum",
                    "name": "Flavor",
                    "namespace": "records.nested",
                    "symbols": [
                        "VANILLA",
                        "CHOCOLATE",
                        "STRAWBERRY"
                    ]
                }
            }
        ]
    }
    """

    def __init__(self, obj: Union[str, dict, 'RecordWithEnum']) -> None:
        if isinstance(obj, str):
            obj = json.loads(obj)

        elif isinstance(obj, type(self)):
            obj = obj.__dict__

        elif not isinstance(obj, dict):
            raise TypeError(
                f"{type(obj)} is not in ('str', 'dict', 'RecordWithEnum')"
            )

        self.set_favoriteFlavor(obj.get('favoriteFlavor', None))

    def dict(self):
        return todict(self)

    def set_favoriteFlavor(self, values: Flavor) -> None:

        self.favoriteFlavor = Flavor(values)

    def get_favoriteFlavor(self) -> Flavor:

        return self.favoriteFlavor

    def serialize(self) -> None:
        return json.dumps(self, default=default_json_serialize)
