""" contains helper function for parsing avro schema """

from avro_to_python.utils.exceptions import BadReferenceError
from avro_to_python.utils.avro.primitive_types import PRIMITIVE_TYPE_MAP


def _create_reference(file: dict) -> dict:
    """ creates a reference object for file references

    Parameters
    ----------
        file: dict
            object containing information on a complex avro type to reference

    Returns
    -------
        reference: dict
            object containing reference information
    """
    if any([('name' not in file), ('namespace') not in file]):
        raise BadReferenceError

    reference = {
        'avro_type': 'reference',
        'name': file['name'],
        'namespace': file['namespace']
    }
    return reference


def _get_namespace(obj: dict, parent_namespace: str=None) -> None:
    """ imputes the namespace if it doesn't already exist

    Namespaces follow the following chain of logic:
        - Use a namespace if it exists
        - If no namespace is given:
            - If referenced in a schema, inherit the same namespace as  parent
            - if not referenced in a schema and no parent, namespace = ''
              resembling the root of the input dir.


    Parameters
    ----------
        obj: dict
            serialized object resembling an avsc schema
        parent_namespace: str
            parent object namespace if applicable

    Returns
    -------
        None
    """
    if obj.get('namespace', None):
        return obj['namespace']
    elif parent_namespace:
        return parent_namespace
    else:
        return ''


def get_union_types(
    field: dict,
    PRIMITIVE_TYPE_MAP: dict=PRIMITIVE_TYPE_MAP
) -> str:
    """ Takes a field object and returns the types of the fields

    Parameters
    ----------
        field: dict
            dictionary resembling a field for a union type
        PRIMITIVE_TYPE_MAP: dict
            lookup table mapping avro types to python types

    Returns
    -------
        out_types: str
            comma seperated string of python types
    """

    out_types = []

    for obj in field['types']:

        # primitive type
        if obj['avro_type'] == 'primitive':
            out_types.append(PRIMITIVE_TYPE_MAP.get(obj['type']))

        # reference to a named type
        elif obj['avro_type'] == 'reference':
            out_types.append(obj['name'])

        elif obj['avro_type'] == 'array':
            out_types.append('list')

        else:
            raise ValueError('unsupported type')

    return ','.join(out_types)
