# -*- coding: utf-8 -*-

"""Console script for avro_to_python."""
import os
import sys

import click
from click import Path

from avro_to_python.reader.read import AvscReader
from avro_to_python.writer.writer import AvroWriter


PIP_HELP = 'Make package pip installable using this name.'
AUTHOR_HELP = 'Author name of the pip installable package.'
VERSION_HELP = 'Version of the pip installable package.'
ENCODING_HELP = 'Encoding to use for source and target (overrides system encoding).'


@click.command()
@click.argument('source', type=Path(), default=None)
@click.argument('target', type=Path(), default=None)
@click.option('--pip', type=str, default=None, required=False, show_default=True, help=PIP_HELP)  # NOQA
@click.option('--top_level_package', type=str, default=None, required=False, show_default=True, help=PIP_HELP)  # NOQA
@click.option('--author', type=str, default=None, required=False, show_default=True, help=AUTHOR_HELP)  # NOQA
@click.option('--package_version', type=str, default='0.1.0', required=False, show_default=True, help=VERSION_HELP)  # NOQA
@click.option('--encoding', type=str, default=None, required=False, show_default=True, help=ENCODING_HELP)  # NOQA
def main(source, target, pip=None, top_level_package=None, author=None, package_version=None, encoding=None):
    """avro-to-python: compile avro avsc schemata to python classes
    """

    if os.path.isfile(source):
        reader = AvscReader(file=source, encoding=encoding)
    else:
        reader = AvscReader(directory=source, encoding=encoding)
    reader.read()
    writer = AvroWriter(
        reader.file_tree,
        pip=pip,
        top_level_package=top_level_package,
        author=author,
        package_version=package_version,
        encoding=encoding
    )
    writer.write(root_dir=target)
    del reader
    return 0


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
