""" helper function to handle union field type """

from typing import Tuple

from avro_to_python.classes.field import Field

from avro_to_python.utils.avro.types.type_factory import _get_field_type
from avro_to_python.utils.avro.types.primitive import _primitive_type
from avro_to_python.utils.avro.types.reference import _reference_type
from avro_to_python.utils.avro.types.enum import _enum_field
from avro_to_python.utils.avro.types.record import _record_field
from avro_to_python.utils.avro.types.array import _array_field


def _union_field(field: dict,
                 parent_namespace: str=None,
                 queue: list=None,
                 references: list=[]) -> Tuple[dict, list]:
    """ helper function for adding information to union fields

    If union contains references to embedded enum or record,
    will add that as a new file in the queue.

    Parameters
    ----------
        field: dict
            union field to extract information from
        parent_namespace: str
            name of parent file namespace
        queue: list
            queue of files to add to project
        references: list
            list of references already made in file

    Returns
    -------
        field_object: dict
            object containing necessary info on union field

        references: potential imports object if a file is generated
    """
    # python is annoying with mutability of this dict
    kwargs = {
        'name': field['name'],
        'fieldtype': 'union',
        'avrotype': None,
        'default': field.get('default', None),
        'reference_name': None,
        'reference_namespace': None,
        'array_item_type': None,
        'union_types': []
    }

    # iterate through possibly types
    for typ in field['type']:
        field_type = _get_field_type(
            field={'type': typ},
            references=references
        )

        # primitive types
        if field_type == 'primitive':
            kwargs['union_types'].append(_primitive_type({
                'name': 'uniontype',
                'type': typ
            }))

        # nested complex record
        elif field_type == 'record':
            kwargs['union_types'].append(_record_field(
                field={'name': 'uniontype', 'type': typ},
                parent_namespace=parent_namespace,
                queue=queue,
                references=references
            ))

        elif field_type == 'array':
            kwargs['union_types'].append(_array_field(field={'name': 'arraytype', 'type': typ}, parent_namespace=parent_namespace, queue=queue, references=references))

        # nested complex record
        elif field_type == 'enum':
            kwargs['union_types'].append(_enum_field(
                field={'name': 'uniontype', 'type': typ},
                parent_namespace=parent_namespace,
                queue=queue,
                references=references
            ))

        # references to previously defined complex types
        # handle reference types
        elif field_type == 'reference':
            kwargs['union_types'].append(_reference_type(
                field={'name': 'uniontype',
                       'type': typ},
                references=references
            ))

        else:
            import pdb; pdb.set_trace()
            raise ValueError(
                f"avro type {field['items']['type']} is not supported"
            )

    return Field(**kwargs)
