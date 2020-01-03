""" helper function for generating a record file """

from typing import List

from avro_to_python.utils.avro.types.array import _array_field
from avro_to_python.utils.avro.types.enum import _enum_field
from avro_to_python.utils.avro.types.record import _record_field
from avro_to_python.utils.avro.types.primitive import _primitive_type
from avro_to_python.utils.avro.types.reference import _reference_type
from avro_to_python.utils.avro.types.type_factory import _get_field_type
from avro_to_python.utils.avro.types.union import _union_field


def _record_file(file: dict, item: dict, queue: List[dict]) -> None:
    """ function for adding information for record files

    Parameters
    ----------
        file: dict
            file object containing information from the avro schema
        item: dict
            object to be turned into a file
        queue: list
            array of file objects to be processed

    Returns
    -------
        None
    """
    file['fields'] = {}
    references = []
    for field in item['fields']:

        field_type = _get_field_type(
            field=field,
            references=references
        )

        # add field name and move into field
        file['fields'][field['name']] = {}

        if field_type == 'array':
            field_object, references = _array_field(
                field=field['type'],
                parent_namespace=file['namespace'],
                queue=queue
            )

        # nested complex record
        elif field_type == 'record':
            field_object, references = _record_field(
                field=field['type'],
                parent_namespace=file['namespace'],
                queue=queue
            )

        # nested complex record
        elif field_type == 'enum':
            field_object, references = _enum_field(
                field=field['type'],
                parent_namespace=file['namespace'],
                queue=queue
            )

        # handle union type
        elif field_type == 'union':
            field_object, references = _union_field(
                field=field,
                parent_namespace=file['namespace'],
                queue=queue,
                references=references
            )

        elif field_type == 'reference':
            reference = [ref for ref in references
                         if ref['name'] == field['type']][0]

            field_object = _reference_type(
                field=field,
                reference=reference
            )

        # handle primitive types
        elif field_type == 'primitive':
            field_object = _primitive_type(field)

        file['fields'][field['name']] = field_object
        file['imports'] += references
