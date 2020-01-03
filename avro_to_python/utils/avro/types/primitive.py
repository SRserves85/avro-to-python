""" file containing primitive type helper function """

from typing import Union


def _primitive_type(field: Union[dict, str]) -> dict:
    """ Function to add information to primitive type fields

    Parameters
    ----------
        field: dict or string
            field object with information on field

    Returns
    -------
        field_object: dict
            object with necessary information on field type information
    """
    if isinstance(field, dict):
        if field.get('type', None) == 'array':
            return {
                'avro_type': 'primitive',
                'type': field['items']['type'],
                'default': field.get('default', None)
            }
        if isinstance(field.get('type'), dict):
            if field.get('type', {}).get('logicalType'):
                return {
                    'avro_type': 'primitive',
                    'type': field['type']['type'],
                    'default': None
                }
        else:
            return {
                'avro_type': 'primitive',
                'type': field['type'],
                'default': field.get('default', None)
            }
    elif isinstance(field, str):
        return {
            'avro_type': 'primitive',
            'type': field,
            'default': None
        }
    else:
        raise ValueError(
            f'{type(field)} is not in (dict, str)'
        )
