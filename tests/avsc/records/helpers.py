""" helper files for avro serialization """

from enum import Enum, EnumMeta
from base64 import b64encode, b64decode


def default_json_serialize(obj):
    """ Wrapper for serializing enum and bytes types"""
    if isinstance(obj, Enum):
        return obj.name
    elif isinstance(obj, bytes):
        return b64encode(obj).decode('utf-8')
    else:
        return obj.__dict__


def default_json_deserialize(obj, targetType):
    """ Wrapper for deserializing bytes type"""
    if isinstance(obj, str) and targetType == bytes:
        return b64decode(obj)
    elif targetType == float:
        return float(obj)
    else:
        return obj


def todict(obj, classkey=None):
    """ helper function to convert nested objects to dicts """
    if isinstance(obj, dict):
        data = {}
        for (k, v) in obj.items():
            data[k] = todict(v, classkey)
        return data
    elif isinstance(obj, Enum):
        return obj.value
    elif hasattr(obj, "_ast"):
        return todict(obj._ast())
    elif hasattr(obj, "__iter__") and not isinstance(obj, str):
        return [todict(v, classkey) for v in obj]
    elif hasattr(obj, "__dict__"):
        data = dict([(key, todict(value, classkey))
                     for key, value in obj.__dict__.items()
                     if not callable(value) and not key.startswith('_')])
        if classkey is not None and hasattr(obj, "__class__"):
            data[classkey] = obj.__class__.__name__
        return data
    else:
        return obj


class DefaultEnumMeta(EnumMeta):
    default = object()

    def __call__(cls, value=default, *args, **kwargs):
        if value is DefaultEnumMeta.default:
            # Assume the first enum is default
            return next(iter(cls))
        return super().__call__(value, *args, **kwargs)


def is_assignable(obj: object, impl_class: type) -> bool:
    """ Determines if an object is assignable to an implementation class by either
    being an instance of such class or a dictionary matching some rules. Currently
    only rules for GeoJson objects are supported.

    Parameters
    ----------
        obj: object
            input object to match
        impl_class: type
            implementation class to match

    Returns
    -------
        out_type: bool
            True if conditions are met
    """
    if isinstance(obj, impl_class):
        return True
    elif isinstance(obj, dict):
        return _is_dict_assignable(obj, impl_class)
    else:
        return False


def _is_dict_assignable(data: dict, impl_class: type) -> bool:
    name = impl_class.__name__
    rule = _IMPLEMENTATION_RULES.get(name)

    # If no rule is defined, fallback to normal implementation, any dict should be assignable to
    # the object. When rule is present, first check the precondition (all specified fields must be present). If
    # not met, result is equivalent to having no rule at all. And finally if precondition is met the specified
    # field must match the indicated value
    return not rule or data.keys() < rule["field_names"] or data[rule["field_match"]] == name


_GEOJSON_GEOMETRY_RULE: dict = {
    "field_names": {"coordinates", "type"},
    "field_match": "type"
}

# Implementation rules to determine if a dict complies with
# implementation class. Currently only GeoJson objects are
# considered, but it could be extended in a more generic way
_IMPLEMENTATION_RULES: dict = {
    "Point": _GEOJSON_GEOMETRY_RULE,
    "LineString": _GEOJSON_GEOMETRY_RULE,
    "Polygon": _GEOJSON_GEOMETRY_RULE,
    "MultiPoint": _GEOJSON_GEOMETRY_RULE,
    "MultiLineString": _GEOJSON_GEOMETRY_RULE,
    "MultiPolygon": _GEOJSON_GEOMETRY_RULE
}

