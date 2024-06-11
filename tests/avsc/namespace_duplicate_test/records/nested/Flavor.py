# -*- coding: utf-8 -*-

""" avro python class for file: Flavor """

import json
from enum import Enum
from helpers import default_json_serialize, DefaultEnumMeta, todict


class Flavor(Enum, metaclass=DefaultEnumMeta):

    schema = """
    {
        "type": "enum",
        "name": "Flavor",
        "namespace": "records.nested",
        "symbols": [
            "VANILLA",
            "CHOCOLATE",
            "STRAWBERRY"
        ]
    }
    """

    VANILLA = 'VANILLA'
    CHOCOLATE = 'CHOCOLATE'
    STRAWBERRY = 'STRAWBERRY'

    def encode(self):
        return self.name

    def serialize(self) -> None:
        return json.dumps(self, default=default_json_serialize)
