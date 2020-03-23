""" helper function to handle map field type """

from typing import Tuple

from avro_to_python.classes.field import Field

from avro_to_python.utils.avro.types.type_factory import _get_field_type
from avro_to_python.utils.avro.types.primitive import _primitive_type
from avro_to_python.utils.avro.types.reference import _reference_type
from avro_to_python.utils.avro.types.enum import _enum_field
from avro_to_python.utils.avro.types.record import _record_field
from avro_to_python.utils.avro.types.array import _array_field

def _map_field(field: dict,
               parent_namespace: str=None,
               queue: list=None,
               references: list=[]) -> Tuple[dict, list]:
    """ helper function for adding information to map fields

    If map contains references to embedded enum or record,
    will add that as a new file in the queue.

    Parameters
    ----------
        field: dict
            map field to extract information from
        parent_namespace: str
            name of parent file namespace
        queue: list
            queue of files to add to project
        references: list
            list of references already made in file

    Returns
    -------
        Field
    """
    # python is annoying with mutability of this dict
    kwargs = {
        'name': field['name'],
        'fieldtype': 'map',
        'avrotype': None,
        'default': field.get('default', None),
        'reference_name': None,
        'reference_namespace': None,
        'array_item_type': None,
        'union_types': [],
        'map_type': None
    }

    if isinstance(field['type']['values'], str):
        map_type = _get_field_type(
            {'type': field['type']['values']},
            references
        )

    else:
        map_type = _get_field_type(
            field['type']['values'],
            references
        )

    # handle primitive types
    if map_type == 'primitive':
        kwargs.update({
            'map_type': _primitive_type(
                {'name': 'maptype', 'type': field['type']['values']}
            )
        })

    # handle complex types
    elif map_type == 'record':
        # array fields don't have names and type need to be nested
        kwargs.update({
            'map_type': _record_field(
                field={'name': 'mapfield', 'type': field['type']['values'], 'namespace': field['type']['values'].get('namespace', None)},
                parent_namespace=parent_namespace,
                queue=queue, references=references)
        })

    elif map_type == 'enum':
        # array fields don't have names and type need to be nested
        kwargs.update({
            'map_type': _enum_field(
                field={'name': 'mapfield', 'type': field['type']['values'], 'namespace': field['type']['values'].get('namespace', None)},
                parent_namespace=parent_namespace,
                queue=queue, references=references)
        })

    elif map_type == 'map':
        # handle nested maps
        kwargs.update({
            'map_type': _map_field(
                field={'name': 'nestedMap', 'type': field['type']['values'], 'namespace''namespace': field['type']['values'].get('namespace', None)},
                parent_namespace=parent_namespace,
                queue=queue, references=references
            )
        })

    elif map_type == 'array':
        # handle nested arrays
        kwargs.update({
            'map_type': _array_field(
                field={'name': 'nestedMap', 'type': field['type']['values'], 'namespace''namespace': field['type']['values'].get('namespace', None)},
                parent_namespace=parent_namespace,
                queue=queue, references=references
            )
        })

    # handle reference types
    elif map_type == 'reference':
        kwargs.update({
            'map_type': _reference_type(
                field={'name': field['type']['values']},
                references=references)
        })

    else:
        raise ValueError(
            f"avro type {field['type']['values']} is not supported"
        )

    return Field(**kwargs)
