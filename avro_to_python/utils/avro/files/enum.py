""" Contains hidden functions to handle enum file type """


def _enum_file(file: dict) -> None:
    """ Function to format enum field object

    Parameters
    ----------
        file: dict
            file object containing information on enum file

    """
    # add symbol and file informatio
    file['symbols'] = file['schema']['symbols']
    file['default'] = file['schema'].get('default', None)
