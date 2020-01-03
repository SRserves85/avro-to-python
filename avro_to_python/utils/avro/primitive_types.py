""" file containing primitive types for avro """

PRIMITIVE_TYPES = {
    'null',
    'boolean',
    'int',
    'long',
    'float',
    'double',
    'bytes',
    'string'
}

PRIMITIVE_TYPE_MAP = {
    'null': 'None',
    'boolean': 'bool',
    'int': 'int',
    'long': 'int',
    'float': 'float',
    'double': 'float',
    'bytes': 'bytes',
    'string': 'str'
}
