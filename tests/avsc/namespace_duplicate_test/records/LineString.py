# -*- coding: utf-8 -*-

""" avro python class for file: LineString """

import json
from helpers import default_json_serialize, default_json_deserialize, todict, is_assignable
from typing import Union


class LineString(object):

    schema = """
    {
        "type": "record",
        "name": "LineString",
        "fields": [
            {
                "name": "bbox",
                "type": [
                    "null",
                    {
                        "type": "array",
                        "items": {
                            "type": "double",
                            "name": null
                        },
                        "java-class": "[D"
                    }
                ],
                "default": null
            },
            {
                "name": "coordinates",
                "type": {
                    "type": "array",
                    "items": {
                        "type": "array",
                        "items": {
                            "type": "double",
                            "name": null
                        },
                        "java-class": "[D"
                    },
                    "java-class": "[[D"
                }
            },
            {
                "name": "type",
                "type": "string"
            }
        ],
        "namespace": "records"
    }
    """

    def __init__(self, obj: Union[str, dict, 'LineString'] = None) -> None:
        if obj is None:
            return

        if isinstance(obj, str):
            obj = json.loads(obj)

        elif isinstance(obj, type(self)):
            obj = obj.__dict__

        elif not isinstance(obj, dict):
            raise TypeError(
                f"{type(obj)} is not in ('str', 'dict', 'LineString')"
            )

        self.set_bbox(obj.get('bbox', None))

        self.set_coordinates(obj.get('coordinates', None))

        self.set_type(default_json_deserialize(obj.get('type', None), str))

    def dict(self):
        return todict(self)

    def set_bbox(self, value: Union[None, list]) -> None:
        if value is None:
            self.bbox = None

        elif isinstance(value, list):
            self.bbox = []
            for element in value:
                if isinstance(element, (float, int)):
                    self.bbox.append(element)
                else:
                    raise TypeError(
                        f"Type for 'bbox' should be '(float, int)' but was: {element}"
                    )
        else:
            raise TypeError(f"field 'bbox' should be in (None, list) but was: {value}")

    def get_bbox(self) -> Union[None, list]:
        return self.bbox

    def set_coordinates(self, values: list) -> None:
        self.coordinates = []
        if isinstance(values, list):
            for element in values:
                self.coordinates.append(element)
        else:
            raise TypeError(f"Field 'coordinates' should be type list but was: {values}")

    def get_coordinates(self) -> list:
        return self.coordinates

    def set_type(self, value: str) -> None:
        if isinstance(value, str):
            self.type = value
        else:
            raise TypeError(f"field 'type' should be type str but was: {value}")

    def get_type(self) -> str:
        return self.type

    def serialize(self) -> None:
        return json.dumps(self, default=default_json_serialize)
