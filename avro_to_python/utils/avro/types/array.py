""" helper function to handle array field type """

from typing import Tuple

from avro_to_python.utils.avro.helpers import (
    _create_reference, _get_namespace
)
from avro_to_python.utils.avro.types.primitive import _primitive_type
from avro_to_python.utils.avro.types.type_factory import _get_field_type
from avro_to_python.utils.avro.types.reference import _reference_type


def _array_field(field: dict,
                 parent_namespace: str=None,
                 queue: list=None,
                 references: list=None) -> Tuple[dict, list]:
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

    Returns
    -------
        field_object: dict
            object containing necessary info on array field
        references: list
            reference object for doing file imports
    """

    field_object = {
        'avro_type': 'array'
    }
    reference = []

    if isinstance(field['items'], str):
        field['items'] = {'type': field['items']}

    field_item_type = _get_field_type(
        field['items'],
        references
    )

    # handle primitive types
    if field_item_type == 'primitive':
        field_object['items'] = _primitive_type(field)
        return field_object, reference

    # handle complex types
    elif field_item_type in ('record', 'enum'):

        field['items']['namespace'] = _get_namespace(
            obj=field['items'],
            parent_namespace=parent_namespace
        )
        reference = _create_reference(field['items'])
        field_object['items'] = reference
        queue.append(field['items'])
        return field_object, [reference]

    elif field_item_type == 'reference':
        old_reference = [ref for ref in references
                         if ref['name'] == field['type']][0]
        field_object['items'] = _reference_type(
            field=field['items'],
            reference=old_reference
        )
        return field_object, reference

    else:
        raise ValueError(
            f"avro type {field['items']['type']} is not supported"
        )
