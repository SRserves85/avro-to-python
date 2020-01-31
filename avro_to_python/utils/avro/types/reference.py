""" function for handling referenced names in records files """


from avro_to_python.classes.field import Field
from avro_to_python.classes.reference import Reference

from avro_to_python.utils.avro.helpers import split_namespace


def _reference_type(field: dict, references: list) -> Field:
    """ Should take reference to another file already created
        and return reference object with proper name

    Parameters
    ----------
        field: dict
            field object to create reference for
        reference: dict
            reference object created early in file field

    Returns
    -------
        Field
    """
    reference = None
    for reference in references:
        if reference.name == field['name']:
            break

    # should only happen with array field references
    if not reference:
        namespace, name = split_namespace(field['type'])
        reference = Reference(name=name, namespace=namespace)
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
