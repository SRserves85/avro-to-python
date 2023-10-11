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
