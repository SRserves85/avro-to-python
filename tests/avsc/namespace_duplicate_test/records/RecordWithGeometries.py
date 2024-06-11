# -*- coding: utf-8 -*-

""" avro python class for file: RecordWithGeometries """

import json
from helpers import default_json_serialize, default_json_deserialize, todict, is_assignable
from typing import Union
from records.Point import Point
from records.LineString import LineString


class RecordWithGeometries(object):

    schema = """
    {
        "type": "record",
        "name": "RecordWithGeometries",
        "namespace": "records",
        "fields": [
            {
                "name": "geometries",
                "type": [
                    "null",
                    {
                        "type": "array",
                        "items": [
                            {
                                "name": "Point",
                                "type": "record",
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
                                                "type": "double",
                                                "name": null
                                            },
                                            "java-class": "[D"
                                        }
                                    },
                                    {
                                        "name": "type",
                                        "type": "string"
                                    }
                                ],
                                "namespace": "records"
                            },
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
                        ],
                        "default": null
                    }
                ],
                "default": null
            }
        ]
    }
    """

    def __init__(self, obj: Union[str, dict, 'RecordWithGeometries'] = None) -> None:
        if obj is None:
            return

        if isinstance(obj, str):
            obj = json.loads(obj)

        elif isinstance(obj, type(self)):
            obj = obj.__dict__

        elif not isinstance(obj, dict):
            raise TypeError(
                f"{type(obj)} is not in ('str', 'dict', 'RecordWithGeometries')"
            )

        self.set_geometries(obj.get('geometries', None))

    def dict(self):
        return todict(self)

    def set_geometries(self, value: Union[None, list]) -> None:
        if value is None:
            self.geometries = None

        elif isinstance(value, list):
            self.geometries = []
            for element in value:
                if is_assignable(element, Point):
                    self.geometries.append(Point(element))
                
                elif is_assignable(element, LineString):
                    self.geometries.append(LineString(element))
        else:
            raise TypeError(f"field 'geometries' should be in (None, list) but was: {value}")

    def get_geometries(self) -> Union[None, list]:
        return self.geometries

    def serialize(self) -> None:
        return json.dumps(self, default=default_json_serialize)
