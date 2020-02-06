""" base Field class for avro field structure """

from typing import Union, List


class Field(object):

    name = None
    fieldtype = None
    avrotype = None
    default = None
    reference_name = None
    reference_namespace = None
    array_item_type = None
    union_types = None
    map_type = None

    def __init__(self, name: str, fieldtype: str, avrotype: str=None,
                 default: Union[int, str, float, dict, None]=None,
                 reference_name: str=None, reference_namespace: str=None,
                 array_item_type: 'Field'=None, union_types: List['Field']=[],
                 map_type: 'Field'=None
                 ):
        self.name = name
        self.fieldtype = fieldtype
        self.avrotype = avrotype
        self.default = default
        self.reference_name = reference_name
        self.reference_namespace = reference_namespace
        self.array_item_type = array_item_type
        self.union_types = union_types
        self.map_type = map_type

    def __eq__(self, other: Union['Field', str]):
        if isinstance(other, Field):
            return self.name == other.name
        elif isinstance(other, str):
            return self.name == other

    def __repr__(self):
        return f"<FieldObject:'{self.name}'>"
