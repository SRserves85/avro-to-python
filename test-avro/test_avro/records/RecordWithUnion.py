# -*- coding: utf-8 -*-

""" avro python class for file: RecordWithUnion """

import json
from test_avro.helpers import default_json_serialize, todict
from typing import Union
from test_avro.records.Thing import Thing


class RecordWithUnion(object):

    schema = """
    {
        "type": "record",
        "name": "RecordWithUnion",
        "namespace": "records",
        "fields": [
            {
                "name": "optionalString",
                "type": [
                    "string",
                    "null"
                ]
            },
            {
                "name": "intOrThing",
                "type": [
                    "int",
                    {
                        "type": "record",
                        "name": "Thing",
                        "fields": [
                            {
                                "name": "id",
                                "type": "int"
                            }
                        ],
                        "namespace": "records"
                    }
                ]
            }
        ]
    }
    """

    def __init__(self, obj: Union[str, dict, 'RecordWithUnion']) -> None:
        if isinstance(obj, str):
            obj = json.loads(obj)

        elif isinstance(obj, type(self)):
            obj = obj.__dict__

        elif not isinstance(obj, dict):
            raise TypeError(
                f"{type(obj)} is not in ('str', 'dict', 'RecordWithUnion')"
            )

        self.set_optionalString(obj.get('optionalString', None))

        self.set_intOrThing(obj.get('intOrThing', None))

    def dict(self):
        return todict(self)

    def set_optionalString(self, value: Union[str, None]) -> None:
        if isinstance(value, str):
            self.optionalString = str(value)

        elif isinstance(value, type(None)):
            self.optionalString = None

        else:
            raise TypeError("field 'optionalString' should be in (str, None)")

    def get_optionalString(self) -> Union[str, None]:
        return self.optionalString

    def set_intOrThing(self, value: Union[int, Thing]) -> None:
        if isinstance(value, int):
            self.intOrThing = int(value)

        elif isinstance(value, (dict, Thing)):
            self.intOrThing = Thing(value)

        else:
            raise TypeError("field 'intOrThing' should be in (int, Thing)")

    def get_intOrThing(self) -> Union[int, Thing]:
        return self.intOrThing

    def serialize(self) -> None:
        return json.dumps(self, default=default_json_serialize)
