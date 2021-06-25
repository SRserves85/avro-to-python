# -*- coding: utf-8 -*-

"""Console script for avro_to_python."""
import os
import sys

import click
from click import Path

from avro_to_python.reader.read import AvscReader
from avro_to_python.writer.writer import AvroWriter


PIP_HELP = 'make package pip installable using this name'
AUTHOR_HELP = 'author name of the pip installable package'
VERSION_HELP = 'version of the pip intallable package'


@click.command()
@click.argument('source', type=Path(), default=None)
@click.argument('target', type=Path(), default=None)
@click.option('--pip', type=str, default=None, required=False, show_default=True, help=PIP_HELP)  # NOQA
@click.option('--author', type=str, default=None, required=False, show_default=True, help=AUTHOR_HELP)  # NOQA
@click.option('--package_version', type=str, default='0.1.0', required=False, show_default=True, help=VERSION_HELP)  # NOQA
def main(source, target, pip=None, author=None, package_version=None):
    """avro-to-python: compile avro avsc schemata to python classes
    """

    if os.path.isfile(source):
        reader = AvscReader(file=source)
    else:
        reader = AvscReader(directory=source)
    reader.read()
    writer = AvroWriter(
        reader.file_tree,
        pip=pip,
        author=author,
        package_version=package_version
    )
    writer.write(root_dir=target)
    del reader
    return 0


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
