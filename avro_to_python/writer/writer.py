""" Writer class for writing python avro files """

import json

from jinja2 import Environment, FileSystemLoader

from avro_to_python.classes.node import Node
from avro_to_python.utils.avro.helpers import get_union_types
from avro_to_python.utils.avro.primitive_types import PRIMITIVE_TYPE_MAP
from avro_to_python.utils.paths import (
    get_system_path, verify_or_create_namespace_path, get_or_create_path
)


TEMPLATE_PATH = __file__.replace('writer/writer.py', 'templates/')
TEMPLATE_PATH = get_system_path(TEMPLATE_PATH)


class AvroWriter(object):
    """ writer class for writing python files

    Should initiate around a tree object with nodes as:

    {
        'children': {},
        'files': {},
        'visited': False
    }

    The "keys" of the children are the namespace names along avro
    namespace paths. The Files are the actual files within the
    namespace that need to be compiled.

    Note: The visited flag in each node is only for node traversal.

    This results in the following behavior given this sample tree:

    tree = {
        'children': {'test': {
            'children': {},
            'files': {'NestedTest': ...},
            'visited': False
        }},
        'files': {'Test' ...},
        'visited': False
    }

    files generated:
    /Test.py
    /test/NestedTest.py
    """
    root_dir = None
    files = []

    def __init__(self, tree: dict, pip: str=None, author: str=None,
                 package_version: str=None) -> None:
        """ Parses tree structured dictionaries into python files

        Parameters
        ----------
            tree: dict
                tree object
                acyclic tree representing a read avro schema namespace
            pip: str
                pip package name
            author: str
                author of pip package

        Returns
        -------
            None

        TODO: Check tree is valid
        """
        self.pip = pip
        self.author = author
        self.package_version = package_version
        self.tree = tree

        # jinja2 templates
        self.template_env = Environment(loader=FileSystemLoader(TEMPLATE_PATH))
        self.template = self.template_env.get_template('baseTemplate.j2')

    def write(self, root_dir: str) -> None:
        """ Public runner method for writing all files in a tree

        Parameters
        ----------
            root_path: str
                root path to write files to

        Returns
        -------
            None
        """

        self.root_dir = get_system_path(root_dir)
        if self.pip:
            self.pip_import = self.pip.replace('-', '_') + '.'
            self.pip_dir = self.root_dir + '/' + self.pip
            self.root_dir += '/' + self.pip + '/' + self.pip.replace('-', '_')
            self.pip = self.pip.replace('-', '_')
        else:
            self.pip_import = ''
        get_or_create_path(self.root_dir)
        self._write_helper_file()

        self._reset_tree()
        self._dfs(self.tree)

        if self.pip:
            self._write_setup_file()
            self._write_pip_init_file()
            self._write_manifest_file()

    def _write_manifest_file(self) -> None:
        """ writes manifest to recursively include packages """
        filepath = self.pip_dir + '/MANIFEST.in'
        template = self.template_env.get_template('files/manifest.j2')
        filetext = template.render(
            pip = self.pip
        )
        with open(filepath, 'w') as f:
            f.write(filetext)

    def _write_setup_file(self) -> None:
        """ writes the setup.py file to the pip dir"""
        filepath = self.pip_dir + '/setup.py'
        template = self.template_env.get_template('files/setup.j2')
        filetext = template.render(
            pip=self.pip,
            author=self.author,
            package_version=self.package_version
        )
        with open(filepath, 'w') as f:
            f.write(filetext)

    def _write_pip_init_file(self) -> None:
        """ writes the __init__ file to the pip dir"""
        filepath = self.pip_dir + '/' + self.pip + '/__init__.py'
        template = self.template_env.get_template('files/pip_init.j2')
        filetext = template.render(
            pip=self.pip,
            author=self.author,
            package_version=self.package_version
        )
        with open(filepath, 'w') as f:
            f.write(filetext)

    def _write_helper_file(self) -> None:
        """ writes the helper file to the root dir """
        filepath = self.root_dir + '/helpers.py'
        template = self.template_env.get_template('files/helpers.j2')
        filetext = template.render()
        with open(filepath, 'w') as f:
            f.write(filetext)

    def _write_init_file(self, imports: set, namespace: str) -> None:
        """ writes __init__.py files for namespace imports"""
        template = self.template_env.get_template('files/init.j2')
        filetext = template.render(
            imports=imports,
            pip_import=self.pip_import
        )
        verify_or_create_namespace_path(
            rootdir=self.root_dir,
            namespace=namespace
        )
        filepath = self.root_dir + namespace.replace('.', '/') + '/' + '__init__.py'  # NOQA
        with open(filepath, 'w') as f:
            f.write(filetext)

    def _write_file(
        self, filename: str, filetext: str, namespace: str
    ) -> None:
        """ writes python filetext to appropriate namespace
        """
        verify_or_create_namespace_path(
            rootdir=self.root_dir,
            namespace=namespace
        )
        filepath = self.root_dir + namespace.replace('.', '/') + '/' + filename + '.py'  # NOQA
        with open(filepath, 'w') as f:
            f.write(filetext)

    def _render_file(self, file: dict) -> str:
        """ compiles a file obj into python

        Parameters
        ----------
            file: dict
                file obj representing an avro file

        Returns
        -------
            filetext: str
                rendered python file as a sting
        """
        filetext = self.template.render(
            file=file,
            primitive_type_map=PRIMITIVE_TYPE_MAP,
            get_union_types=get_union_types,
            json=json,
            pip_import=self.pip_import,
            enumerate=enumerate
        )
        return filetext

    def _reset_tree(self, node: Node=None) -> None:
        """ resets the visited flags in node objects

        Parameters
        ----------
            node:
                Node

        Returns
        -------
            None
        """
        # mark as visited
        if not node:
            node = self.tree

        node.visited = False

        for name in node.children:
            if node.children[name].visited:
                self._reset_tree(node=node.children[name])

    def _dfs(self, node: Node=None, namespace: str='') -> None:
        """ yields files from tree via DFS

        Parameters
        ----------
            node: Node
               node in graph for traversal
               if not specified, will use root of tree

        Returns
        -------
            file: dict
                file object representing avro record or enum
        """

        # initialize stack from root node

        # mark as visited
        if not node:
            node = self.tree

        node.visited = True

        imports = set()
        for filename, file in node.files.items():
            filetext = self._render_file(file=file)
            self._write_file(
                filename=filename,
                filetext=filetext,
                namespace=namespace
            )
            imports.add(
                file.namespace + '.' + file.name
            )

        # add __init__ files for correct imports
        self._write_init_file(
            imports=imports, namespace=namespace
        )

        # add non-visited children to stack
        for name in node.children:
            if not node.children[name].visited:
                self._dfs(
                    node=node.children[name],
                    namespace=namespace + '.' + name
                )
