""" handles situation where enum file is referenced in schema """


from typing import Tuple

from avro_to_python.classes.field import Field

from avro_to_python.utils.avro.helpers import (
    _get_namespace, _create_reference
)


kwargs = {
    'name': None,
    'fieldtype': None,
    'avrotype': None,
    'default': None,
    'reference_name': None,
    'reference_namespace': None
}


def _enum_field(field: dict,
                parent_namespace: str=None,
                queue: list=None,
                references: list=None) -> Tuple[dict, list]:
    """ helper function for adding information to nested enum field

    will add field as a new file in the queue and will be referenced.

    Parameters
    ----------
        field: dict
           field object to extract information from
        queue: list
            queue of files to add to project

    Returns
    -------
        Field
    """
    field['type']['namespace'] = _get_namespace(obj=field['type'], parent_namespace=parent_namespace)
    reference = _create_reference(field['type'])
    references.append(reference)

    queue.append(field['type'])

    kwargs.update({
        'name': field['name'],
        'reference_name': reference.name,
        'reference_namespace': reference.namespace,
        'fieldtype': 'reference',
        'default': field.get('default', None)
    })

    return Field(**kwargs)
