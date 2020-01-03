""" helper function to handle union field type """
from typing import Tuple


from avro_to_python.utils.avro.types.type_factory import _get_field_type
from avro_to_python.utils.avro.types.primitive import _primitive_type
from avro_to_python.utils.avro.types.reference import _reference_type
from avro_to_python.utils.avro.types.enum import _enum_field
from avro_to_python.utils.avro.types.record import _record_field


def _union_field(field: dict,
                 parent_namespace: str=None,
                 queue: list=None,
                 references: list=None) -> Tuple[dict, list]:
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

    field_object = {
        'avro_type': 'union',
        'types': []
    }
    references = []

    # iterate through possibly types
    for typ in field['type']:
        field_type = _get_field_type(
            field={'type': typ},
            references=references
        )

        # primitive types
        if field_type == 'primitive':
            field_object['types'].append(_primitive_type(typ))

        # nested complex record
        elif field_type == 'record':
            file_obj, file_references = _record_field(
                field=typ,
                parent_namespace=parent_namespace,
                queue=queue
            )
            field_object['types'].append(file_obj)
            if file_references:
                references += file_references

        # nested complex record
        elif field_type == 'enum':
            file_obj, file_references = _enum_field(
                field=typ,
                parent_namespace=parent_namespace,
                queue=queue
            )
            field_object['types'].append(file_obj)
            if file_references:
                references += file_references

        # references to previously defined complex types
        elif field_type == 'reference':
            old_reference = [ref for ref in references
                             if ref['name'] == field['type']][0]
            field_object['items'] = _reference_type(
                field=field['items'],
                reference=old_reference
            )

    return field_object, references
