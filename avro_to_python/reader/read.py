""" contains class and methods for reading avro files and dirs """

import copy
import os
import json

from avro_to_python.utils.paths import (
    get_system_path, get_avsc_files, verify_path_exists
)
from avro_to_python.utils.exceptions import (
    NoFileOrDir, MissingFileError, NoFilesError
)

from avro_to_python.utils.avro.helpers import _get_namespace
from avro_to_python.utils.avro.files.enum import _enum_file
from avro_to_python.utils.avro.files.record import _record_file


class AvscReader(object):
    """
    reader object for avro avsc files

    Should contain all logic for reading and formatting information
    within a dir of avsc files or a single file
    """

    def __init__(self, directory: str=None, file: str=None) -> None:
        """ Initializer should just create a list of files to process

        Parameters
        ----------
            directory: str
                Directory of files to read
                Cannot be used with "file" param

            file: str
                path of avsc file to compile
                Cannot be used with "directory" param

        Returns
        -------
            None
        """

        # initialize cental object
        self.obj = {}

        if directory:
            if os.path.isfile(directory):
                raise OSError(f'{directory} is a file!')
            files = get_avsc_files(directory)
            if files:
                self.files = files
                self.obj['root_dir'] = get_system_path(directory)
                self.obj['read_type'] = 'directory'
            else:
                raise NoFilesError(f'No avsc files found in {directory}')

        elif file:
            if not verify_path_exists(file):
                raise MissingFileError(f'{file} does not exist!')
            if os.path.isdir(file):
                raise IsADirectoryError(f'{file} is a directory!')
            syspath = get_system_path(file)
            self.files = [syspath]
            self.obj['read_type'] = 'file'

        else:
            raise NoFileOrDir

        self.obj['avsc'] = []

    def read(self):
        """ runner method for AvscReader object """
        self._read_files()
        self._build_namespace_tree()

    def _traverse_tree(self, root_node: dict, namespace: str='') -> dict:
        """ Traverses the namespace tree to add files to namespace paths

        Parameters
        ----------
            root_node: dict
                root_node node to start tree traversal
            namespace: str (period seperated)
                namespace representing the tree path

        Returns
        -------
            current_node: dict
                child node in tree representing namespace destination
        """
        current_node = root_node
        nodes = namespace.split('.')

        # empty namespace
        if namespace == '':
            return current_node

        for node in nodes:

            # create node if it doesn't exist
            if node not in current_node['children']:
                current_node['children'][node] = {
                    'children': {},
                    'files': {},
                    'visited': False
                }
            # move through tree
            current_node = current_node['children'][node]

        return current_node

    def _read_files(self) -> None:
        """ reads and serializes avsc files to central object
        """
        for file in self.files:
            with open(file, 'r') as f:
                serialized = json.load(f)
                self.obj['avsc'].append(serialized)

    def _build_namespace_tree(self) -> None:
        """ builds tree structure on namespace
        """
        # think of namespaces as acyclic trees
        root_node = {
            'children': {},
            'files': {},
            'visited': False
        }

        # populate queue prir to tree building
        queue = copy.deepcopy(self.obj['avsc'])

        while queue:

            # get first item in queue
            item = queue.pop(0)

            # impute namespace
            item['namespace'] = _get_namespace(item)

            # traverse to namespace starting from root_node
            current_node = self._traverse_tree(
                root_node=root_node, namespace=item['namespace']
            )

            # create file obj
            current_node['files'][item['name']] = {}
            file = current_node['files'][item['name']]

            # add file information
            file['name'] = item['name']
            file['type'] = item['type']
            file['namespace'] = item['namespace']
            file['schema'] = item
            file['imports'] = []

            # handle record type
            if file['type'] == 'record':
                _record_file(file, item, queue)

            # handle enum type file
            elif file['type'] == 'enum':
                _enum_file(file)
            else:
                raise ValueError(
                    f"{file['type']} is currently not supported."
                )
        self.file_tree = root_node
