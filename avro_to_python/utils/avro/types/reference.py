""" function for handling referenced names in records files """


from avro_to_python.classes.field import Field
from avro_to_python.classes.reference import Reference

from avro_to_python.utils.avro.helpers import split_namespace


def _reference_type(field: dict, references: list, parent_namespace: str = None) -> Field:
    """ Should take reference to another file already created
        and return reference object with proper name

    Parameters
    ----------
        field: dict
            field object to create reference for
        reference: dict
            reference object created early in file field
        parent_namespace: str
            parent object namespace

    Returns
    -------
        Field
    """
    reference = None

    # Applies to field['name'] = 'uniontype' or field['name'] is the name of a field in a record
    if not field.get('type'):
        ref_name = field['name']
        ref_namespace = ''
    elif '.' not in field['name'] and field['name'][0].islower():
        ref_namespace, ref_name = split_namespace(field['type'])
    else:
        ref_name = field['name']
        ref_namespace = field['type']

    # Applies to references in arrays where name indicates type with namespace. In this case
    # ref_namespace contains the namespace of the parent that should only be applied if ref_name
    # does not contain a namespace
    if '.' in ref_name:
        ref_namespace, ref_name = split_namespace(ref_name)
    # It could be that reference does specify namespace, then we must assume parents namespace
    if not ref_namespace and parent_namespace:
        ref_namespace = parent_namespace

    for ref in references:
        if ref.name == ref_name:
            reference = ref
            break

    # should only happen with array field references
    if not reference:
        reference = Reference(name=ref_name, namespace=ref_namespace)
        references.append(reference)

    kwargs = {
        'name': field['name'],
        'fieldtype': 'reference',
        'avrotype': None,
        'reference_name': reference.name,
        'reference_namespace': reference.namespace,
        'default': field.get('default', None)
    }
    return Field(**kwargs)
