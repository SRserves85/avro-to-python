""" contains class and methods for reading avro files and dirs """

import copy
import json
import os

from avro_to_python.classes.field import Field
from avro_to_python.classes.file import File
from avro_to_python.classes.node import Node
from avro_to_python.utils.avro.files.enum import _enum_file
from avro_to_python.utils.avro.files.record import _record_file
from avro_to_python.utils.avro.helpers import _get_name, _get_namespace
from avro_to_python.utils.exceptions import (
    NoFileOrDir, MissingFileError, NoFilesError
)
from avro_to_python.utils.paths import (
    get_system_path, get_avsc_files, verify_path_exists
)


class AvscReader(object):
    """
    reader object for avro avsc files

    Should contain all logic for reading and formatting information
    within a dir of avsc files or a single file
    """
    file_tree = None

    def __init__(self, directory: str=None, file: str=None, encoding: str=None) -> None:
        """ Initializer should just create a list of files to process

        Parameters
        ----------
            directory: str
                Directory of files to read
                Cannot be used with "file" param

            file: str
                path of avsc file to compile
                Cannot be used with "directory" param

            encoding: str
                encoding of the source file(s) (defaults to
                system encoding)

        Returns
        -------
            None
        """

        # initialize cental object
        self.obj = {}
        self.file_tree = None
        self.encoding = encoding
        self.enum_references = set()

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
        namespaces = namespace.split('.')

        # empty namespace
        if namespace == '':
            return current_node

        for name in namespaces:

            # create node if it doesn't exist
            if name not in current_node.children:
                current_node.children[name] = Node(
                    name=name,
                    children={},
                    files={}
                )

            # move through tree
            current_node = current_node.children[name]

        return current_node

    def _read_files(self) -> None:
        """ reads and serializes avsc files to central object
        """
        for file in self.files:
            with open(file, 'r', encoding=self.encoding) as f:
                serialized = json.load(f)
                self.obj['avsc'].append(serialized)

    def _build_namespace_tree(self) -> None:
        """ builds tree structure on namespace
        """
        # initialize empty node with empty string name
        root_node = Node(name='')

        # populate queue prior to tree building
        queue = copy.deepcopy(self.obj['avsc'])

        while queue:

            # get first item in queue
            item = queue.pop(0)

            # impute namespace and name
            item['namespace'] = _get_namespace(item)
            item['name'] = _get_name(item)

            # traverse to namespace starting from root_node
            current_node = self._traverse_tree(
                root_node=root_node, namespace=item['namespace']
            )

            # initialize empty file obj for mutation
            file = File(
                name=item['name'],
                avrotype=item['type'],
                namespace=item['namespace'],
                schema=item,
                fields={},
                imports=[],
                enum_sumbols=[]
            )

            # handle record type
            if file.avrotype == 'record':
                _record_file(file, item, queue)

            # handle enum type file
            elif file.avrotype == 'enum':
                _enum_file(file, item)
                self._add_enum_reference(file)
            else:
                raise ValueError(
                    f"{file['type']} is currently not supported."
                )

            current_node.files[item['name']] = file

        self._process_enum_references_in_node(root_node)
        self.file_tree = root_node

    def _add_enum_reference(self, file:File) -> None:
        self.enum_references.add(f"{file.namespace}.{file.name}")

    def _process_enum_references_in_node(self, node: Node) -> None:
        for file_key in node.files:
            file = node.files[file_key]
            if file.avrotype == 'record':
                for field in file.fields:
                    self._process_enum_references_in_field(file.fields[field])

        for child in node.children:
            self._process_enum_references_in_node(node.children[child])

    def _process_enum_references_in_field(self, field: Field) -> None:
        if field.fieldtype == 'reference':
            self._process_reference(field)
        elif field.fieldtype == 'array':
            self._process_enum_references_in_field(field.array_item_type)
        elif field.fieldtype == 'map':
            self._process_enum_references_in_field(field.map_type)
        elif field.fieldtype == 'union':
            for item in field.union_types:
                self._process_enum_references_in_field(item)

    def _process_reference(self, field:Field) -> None:
        if f"{field.reference_namespace}.{field.reference_name}" in self.enum_references and not field.is_enum:
            field.is_enum = True
