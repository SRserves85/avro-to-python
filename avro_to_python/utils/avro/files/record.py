""" helper function for generating a record file """

from typing import List

from avro_to_python.classes.file import File

from avro_to_python.utils.avro.helpers import dedupe_imports

from avro_to_python.utils.avro.types.array import _array_field
from avro_to_python.utils.avro.types.enum import _enum_field
from avro_to_python.utils.avro.types.record import _record_field
from avro_to_python.utils.avro.types.primitive import _primitive_type
from avro_to_python.utils.avro.types.reference import _reference_type
from avro_to_python.utils.avro.types.type_factory import _get_field_type
from avro_to_python.utils.avro.types.union import _union_field
from avro_to_python.utils.avro.types.map import _map_field


def _record_file(file: File, item: dict, queue: List[dict]) -> None:
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
    references = []
    for field in item['fields']:

        fieldtype = _get_field_type(
            field=field,
            references=references
        )

        if fieldtype == 'array':
            field = _array_field(
                field=field,
                parent_namespace=file.namespace,
                queue=queue,
                references=references
            )

        elif fieldtype == 'map':
            field = _map_field(
                field=field,
                parent_namespace=file.namespace,
                queue=queue,
                references=references
            )

        # nested complex record
        elif fieldtype == 'record':
            field = _record_field(
                field=field,
                parent_namespace=file.namespace,
                queue=queue,
                references=references
            )

        # nested complex record
        elif fieldtype == 'enum':
            field = _enum_field(
                field=field,
                parent_namespace=file.namespace,
                queue=queue,
                references=references
            )

        # handle union type
        elif fieldtype == 'union':
            field = _union_field(
                field=field,
                parent_namespace=file.namespace,
                queue=queue,
                references=references
            )

        elif fieldtype == 'reference':
            field = _reference_type(
                field=field,
                references=references
            )

        # handle primitive types
        elif fieldtype == 'primitive':
            field = _primitive_type(field)

        else:
            raise ValueError('fieldtype is not supported...')

        file.fields[field.name] = field
        file.imports += references

    file.imports = dedupe_imports(file.imports)
