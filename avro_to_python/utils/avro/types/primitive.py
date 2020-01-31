""" file containing primitive type helper function """

from typing import Union

from avro_to_python.utils.avro.primitive_types import PRIMITIVE_TYPES

from avro_to_python.classes.field import Field

kwargs = {
    'name': None,
    'fieldtype': 'primitive',
    'avrotype': None,
    'default': None
}


def _primitive_type(field: Union[dict, str]) -> dict:
    """ Function to add information to primitive type fields

    Parameters
    ----------
        field: dict or string
            field object with information on field

    Returns
    -------

        Field
    """
    kwargs.update({
        'name': field['name'],
        'default': field.get('default', None)
    })

    if isinstance(field, dict):
        if field.get('type', None) == 'array':
                kwargs.update({'avrotype': field['items']['type']})

        elif isinstance(field.get('type'), dict):
            if field.get('type', {}).get('logicalType'):
                kwargs.update({'avrotype': field['type']['type']})

        elif isinstance(field.get('type'), str):
            if field['type'] in PRIMITIVE_TYPES:
                kwargs.update({'avrotype': field['type']})

        else:
            kwargs.update({'avrotype': field['item']['type']})

    elif isinstance(field, str):
        kwargs.update({'avrotype': field['item']['type']})
    else:
        raise ValueError(
            f'{type(field)} is not in (dict, str)'
        )
    return Field(**kwargs)
