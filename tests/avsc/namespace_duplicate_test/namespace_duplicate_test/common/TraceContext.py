# -*- coding: utf-8 -*-

""" avro python class for file: TraceContext """

import json
from helpers import default_json_serialize, default_json_deserialize, todict, is_assignable
from typing import Union


class TraceContext(object):

    schema = """
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
    """

    def __init__(self, obj: Union[str, dict, 'TraceContext'] = None) -> None:
        if obj is None:
            return

        if isinstance(obj, str):
            obj = json.loads(obj)

        elif isinstance(obj, type(self)):
            obj = obj.__dict__

        elif not isinstance(obj, dict):
            raise TypeError(
                f"{type(obj)} is not in ('str', 'dict', 'TraceContext')"
            )

        self.set_traceId(default_json_deserialize(obj.get('traceId', None), str))

    def dict(self):
        return todict(self)

    def set_traceId(self, value: str) -> None:
        if isinstance(value, str):
            self.traceId = value
        else:
            raise TypeError(f"field 'traceId' should be type str but was: {value}")

    def get_traceId(self) -> str:
        return self.traceId

    def serialize(self) -> None:
        return json.dumps(self, default=default_json_serialize)
