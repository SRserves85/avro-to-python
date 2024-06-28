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

# Equivalences for isinstance checks as numbers in JSON can omit fractional part (parsed as int)
IS_INSTANCE_PRIMITIVE_TYPE_MAP = {
    'null': 'None',
    'boolean': 'bool',
    'int': 'int',
    'long': 'int',
    'float': '(float, int)',
    'double': '(float, int)',
    'bytes': 'bytes',
    'string': 'str'
}

IS_INSTANCE_PRIMITIVE_TYPE_EQ_MAP = {
    'None': 'None',
    'bool': 'bool',
    'int': 'int',
    'float': '(float, int)',
    'bytes': 'bytes',
    'str': 'str'
}
