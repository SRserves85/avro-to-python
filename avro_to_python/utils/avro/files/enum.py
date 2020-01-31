""" Contains hidden functions to handle enum file type """


from avro_to_python.classes.file import File


def _enum_file(file: File, item: dict) -> None:
    """ Function to format enum field object

    Parameters
    ----------
        file: File
            file object containing information on enum file

    """
    # add symbol and default information
    file.symbols = item['symbols']
    file.default = item.get('default', None)
