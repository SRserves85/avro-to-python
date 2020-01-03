from typing import Tuple

from avro_to_python.utils.avro.helpers import (
    _get_namespace, _create_reference
)


def _record_field(field: dict,
                  parent_namespace: str=None,
                  queue: list=None) -> Tuple[dict, list]:
    """ helper function for adding information to nested record field

    will add field as a new file in the queue and will be referenced.

    Parameters
    ----------
        field: dict
           field object to extract information from
        queue: list
            queue of files to add to project

    Returns
    -------
        field_object: dict
            object containing necessary info on array field
        references: list
            list of reference objects for importing
    """
    field['namespace'] = _get_namespace(
        obj=field,
        parent_namespace=parent_namespace
    )
    queue.append(field)
    field_object = references = _create_reference(field)

    # add default value if exists
    references.update({
        'default': field.get('default', None)
    })

    return field_object, [references]
