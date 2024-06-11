# -*- coding: utf-8 -*-

""" avro python class for file: Common """

import json
from helpers import default_json_serialize, default_json_deserialize, todict, is_assignable
from typing import Union
from namespace_duplicate_test.common.TraceContext import TraceContext


class Common(object):

    schema = """
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
    """

    def __init__(self, obj: Union[str, dict, 'Common'] = None) -> None:
        if obj is None:
            return

        if isinstance(obj, str):
            obj = json.loads(obj)

        elif isinstance(obj, type(self)):
            obj = obj.__dict__

        elif not isinstance(obj, dict):
            raise TypeError(
                f"{type(obj)} is not in ('str', 'dict', 'Common')"
            )

        self.set_uuid(default_json_deserialize(obj.get('uuid', None), str))

        self.set_trace(obj.get('trace', None))

    def dict(self):
        return todict(self)

    def set_uuid(self, value: str) -> None:
        if isinstance(value, str):
            self.uuid = value
        else:
            raise TypeError(f"field 'uuid' should be type str but was: {value}")

    def get_uuid(self) -> str:
        return self.uuid

    def set_trace(self, value: Union[None, TraceContext]) -> None:
        if value is None:
            self.trace = None

        elif is_assignable(value, TraceContext):
            self.trace = TraceContext(value)
        else:
            raise TypeError(f"field 'trace' should be in (None, TraceContext) but was: {value}")

    def get_trace(self) -> Union[None, TraceContext]:
        return self.trace

    def serialize(self) -> None:
        return json.dumps(self, default=default_json_serialize)
