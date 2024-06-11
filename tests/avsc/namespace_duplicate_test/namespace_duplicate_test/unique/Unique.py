# -*- coding: utf-8 -*-

""" avro python class for file: Unique """

import json
from helpers import default_json_serialize, default_json_deserialize, todict, is_assignable
from typing import Union
from namespace_duplicate_test.common.Common import Common
from namespace_duplicate_test.common.enums.CommonEnum import CommonEnum
from namespace_duplicate_test.unique.UniqueEnum import UniqueEnum


class Unique(object):

    schema = """
    {
        "type": "record",
        "name": "Unique",
        "namespace": "namespace_duplicate_test.unique",
        "fields": [
            {
                "name": "common",
                "type": {
                    "type": "record",
                    "name": "Common",
                    "namespace": "namespace_duplicate_test.common",
                    "fields": [
                        {
                            "name": "uuid",
                            "type": "string"
                        },
                        {
                            "name": "trace",
                            "type": [
                                "null",
                                {
                                    "type": "record",
                                    "name": "TraceContext",
                                    "fields": [
                                        {
                                            "name": "traceId",
                                            "type": "string"
                                        }
                                    ],
                                    "namespace": "namespace_duplicate_test.common"
                                }
                            ],
                            "default": null
                        }
                    ]
                }
            },
            {
                "name": "common",
                "type": [
                    "null",
                    {
                        "type": "record",
                        "name": "Common",
                        "namespace": "namespace_duplicate_test.common",
                        "fields": [
                            {
                                "name": "uuid",
                                "type": "string"
                            },
                            {
                                "name": "trace",
                                "type": [
                                    "null",
                                    {
                                        "type": "record",
                                        "name": "TraceContext",
                                        "fields": [
                                            {
                                                "name": "traceId",
                                                "type": "string"
                                            }
                                        ],
                                        "namespace": "namespace_duplicate_test.common"
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
                "name": "commonenum",
                "type": {
                    "type": "enum",
                    "name": "CommonEnum",
                    "symbols": [
                        "TEST_VAL1",
                        "TEST_VAL2",
                        "OUTDATED_SCHEMA"
                    ],
                    "default": "OUTDATED_SCHEMA",
                    "namespace": "namespace_duplicate_test.common.enums"
                }
            },
            {
                "name": "uniqueenum",
                "type": {
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
            }
        ],
        "default": null
    }
    """

    def __init__(self, obj: Union[str, dict, 'Unique'] = None) -> None:
        if obj is None:
            return

        if isinstance(obj, str):
            obj = json.loads(obj)

        elif isinstance(obj, type(self)):
            obj = obj.__dict__

        elif not isinstance(obj, dict):
            raise TypeError(
                f"{type(obj)} is not in ('str', 'dict', 'Unique')"
            )

        self.set_common(obj.get('common', None))

        self.set_commonenum(obj.get('commonenum', None))

        self.set_uniqueenum(obj.get('uniqueenum', None))

    def dict(self):
        return todict(self)

    def set_common(self, value: Union[None, Common]) -> None:
        if value is None:
            self.common = None

        elif is_assignable(value, Common):
            self.common = Common(value)
        else:
            raise TypeError(f"field 'common' should be in (None, Common) but was: {value}")

    def get_common(self) -> Union[None, Common]:
        return self.common

    def set_commonenum(self, values: CommonEnum) -> None:

        self.commonenum = CommonEnum(values)

    def get_commonenum(self) -> CommonEnum:

        return self.commonenum

    def set_uniqueenum(self, values: UniqueEnum) -> None:

        self.uniqueenum = UniqueEnum(values)

    def get_uniqueenum(self) -> UniqueEnum:

        return self.uniqueenum

    def serialize(self) -> None:
        return json.dumps(self, default=default_json_serialize)
