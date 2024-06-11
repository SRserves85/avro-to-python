# -*- coding: utf-8 -*-

""" avro python class for file: UniqueEnum """

import json
from enum import Enum
from helpers import default_json_serialize, DefaultEnumMeta, todict


class UniqueEnum(Enum, metaclass=DefaultEnumMeta):

    schema = """
    {
        "type": "enum",
        "name": "UniqueEnum",
        "symbols": [
            "TEST_VAL1",
            "TEST_VAL2",
            "OUTDATED_SCHEMA"
        ],
        "default": "OUTDATED_SCHEMA",
        "namespace": "namespace_duplicate_test.unique"
    }
    """

    # the first value (OUTDATED_SCHEMA) is the default
    OUTDATED_SCHEMA = 'OUTDATED_SCHEMA'

    TEST_VAL1 = 'TEST_VAL1'
    TEST_VAL2 = 'TEST_VAL2'

    def encode(self):
        return self.name

    def serialize(self) -> None:
        return json.dumps(self, default=default_json_serialize)
