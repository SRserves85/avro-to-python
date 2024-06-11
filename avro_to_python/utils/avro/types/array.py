""" helper function to handle array field type """

from typing import Tuple

from avro_to_python.classes.field import Field

from avro_to_python.utils.avro.types.primitive import _primitive_type
from avro_to_python.utils.avro.types.record import _record_field
from avro_to_python.utils.avro.types.enum import _enum_field
from avro_to_python.utils.avro.types.reference import _reference_type
from avro_to_python.utils.avro.types.type_factory import _get_field_type


def _array_field(field: dict,
                 parent_namespace: str=None,
                 queue: list=None,
                 references: list=[]) -> Tuple[dict, list]:
    """ helper function for adding information to array fields

    If array contains references to embedded enum or record,
    will add that as a new file in the queue.

    Parameters
    ----------
        field: dict
            array field to extract information from
        parent_namespace: str
            namespace of the parent file
        queue: list
            queue of files to add to project
        references: list

    Returns
    -------
        Field
    """
    kwargs = {
        'name': field['name'],
        'fieldtype': 'array',
        'avrotype': None,
        'default': None,
        'reference_name': None,
        'reference_namespace': None,
        'array_item_type': None
    }

    if isinstance(field['type']['items'], str):
        field['type']['items'] = {'type': field['type']['items']}
    elif isinstance(field['type']['items'], list):
        field['type']['items'] = {'type': field['type']['items']}

    field_item_type = _get_field_type(
        field['type']['items'],
        references
    )

    # handle primitive types
    if field_item_type == 'primitive':
        # add None name to primitive type
        field['type']['items']['name'] = None
        kwargs.update({
            'array_item_type': _primitive_type(field['type']['items'])
        })

    # handle complex types
    elif field_item_type in ['record', 'enum', 'map', 'array', 'union']:
        field_item_namespace = field['type'].get('namespace')

        if field_item_type == 'record':
            _func = _record_field
            field_item_namespace = field['type']['items'].get('namespace')
        elif field_item_type == 'enum':
            _func = _enum_field
        elif field_item_type == 'map':
            # delayed importing to avoid circular dependency, may want to do
            # the same in map.py
            from avro_to_python.utils.avro.types.map import _map_field
            _func = _map_field
        elif field_item_type == 'array':
            _func = _array_field
        elif field_item_type == 'union':
            # delayed importing to avoid circular dependency, may want to do
            # the same in map.py
            from avro_to_python.utils.avro.types.union import _union_field
            field['type']['items'] = field['type']['items']['type']
            _func = _union_field
        else:
            raise ValueError("you shouldn't have been able to get here")
        kwargs.update({'array_item_type': _func(
            field={'name': 'arrayfield',
                   'type': field['type']['items'],
                   'namespace': field_item_namespace},
            parent_namespace=parent_namespace,
            queue=queue, references=references)})

    # handle reference types
    elif field_item_type == 'reference':
        kwargs.update({
            'array_item_type': _reference_type(
                field={'name': field['type']['items']['type'], 'type': parent_namespace},
                references=references)
        })

    else:
        raise ValueError(
            f"avro type array<{field['type']['items']['type']}> is not supported"
        )

    return Field(**kwargs)
