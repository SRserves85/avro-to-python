""" contains function for handling avro field types """


from avro_to_python.utils.avro.primitive_types import PRIMITIVE_TYPES


def _get_field_type(field: dict, references: list=None) -> str:
    """ returns the field type from parsed avro field

    Parameters
    ----------
        field: dict
            field object with hidden type
        references: list
            list of already created references made in file

        type: str
            type of field
            Must be one of (array, primitive, union, enum, record, logical)
    """

    if isinstance(field['type'], dict):

        # nested array
        if field['type']['type'] == 'array':
            return 'array'

        if field['type']['type'] == 'map':
            return 'map'

        # nested record
        elif field['type']['type'] == 'record':
            return 'record'

        # nested enum
        elif field['type']['type'] == 'enum':
            return 'enum'

        # logical_types
        elif field['type'].get('logicalType', None):
            if field['type']['type'] in PRIMITIVE_TYPES:
                return 'primitive'
            else:
                raise ValueError(
                    f'{field["type"]["type"]} is not supported.'
                )

        else:
            raise ValueError(
                f'{field["type"]["type"]} is not supported.'
            )

    # union type
    elif isinstance(field['type'], list):
        return 'union'

    # handle primitive types
    elif isinstance(field['type'], str):
        if field['type'] in PRIMITIVE_TYPES:
            return 'primitive'

        elif field['type'] == 'record':
            return 'record'

        elif field['type'] == 'enum':
            return 'enum'

        elif field['type'] == 'map':
            return 'map'

        elif field['type'] == 'array':
            return 'array'

        # field is a reference to a enum or record
        else:
            return 'reference'

    else:
        raise ValueError(
            f'{field["type"]["type"]} is not supported.'
        )
