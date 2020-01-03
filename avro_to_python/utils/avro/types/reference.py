""" function for handling referenced names in records files """

import copy


def _reference_type(field: dict, reference: dict) -> dict:
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
        field_object: dict
            field object containing reference and any default values
    """
    field_object = copy.deepcopy(reference)
    field_object.update({
        'default': field.get('default', None)
    })
    return field_object
