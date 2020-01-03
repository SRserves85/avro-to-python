""" contains functions to helping find file paths """

import os
from typing import List


def get_avsc_files(directory: str) -> List[str]:
    """ Gets system paths for all avsc files in a dir

    Parameters
    ----------
        directory: str
            dir containing avsc files to be read

    Returns
    -------
        paths: list of str
            system file paths of avsc files in directory

    """
    paths = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.avsc'):
                # get the absolute path of file
                path = os.path.abspath(
                    os.path.join(root, file)
                )
                paths.append(path)
    return paths


def get_system_path(path: str) -> str:
    """ gets system path of a file

    Parameters
    ----------
        path: str
            local path of a file

    Returns
    -------
        syspath: str
            system path of a file

    """
    syspath = os.path.abspath(path)
    return syspath


def verify_path_exists(path: str) -> bool:
    """ verifies path exists

    Parameters
    ----------
        path: str
            path of file to verify

    Returns
    -------
        exists_flag: bool
            boolean if the file exists or not
    """
    exists_flag = os.path.exists(path)
    return exists_flag


def is_avsc_file(path: str) -> bool:
    """ verifies file is avsc file

    TODO: Verify more then just the file path

    Parameters
    ----------
        path: str
            path of file to verify

    Returns
    -------
        avsc_file_flag: bool
            boolean if file is a avsc file
    """
    filename, file_extension = os.path.splitext(path)
    avsc_file_flag = file_extension == '.avsc'
    return avsc_file_flag


def verify_or_create_namespace_path(rootdir: str, namespace: str) -> None:
    """ creates namespace structure in file system

    Parameters
    ----------
        rootdir: str
            root path to start the namespace
        namespace: str
            period seperated namespace to create
    """
    if not verify_path_exists(rootdir):
        raise OSError('root path does not exist.')

    namespace_path = rootdir + namespace.replace('.', '/') + '/'
    os.makedirs(namespace_path, exist_ok=True)


def get_or_create_path(path: str) -> None:
    """ Gets or created a specified sys path

    The python "os.makedirs" recursively makes paths.

    Parameters
    ----------
        path: str
            path to be verified or created
            can be relative or sys path

    Returns
    -------
        None
    """
    syspath = get_system_path(path)
    os.makedirs(syspath, exist_ok=True)
