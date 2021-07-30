import json
import os
import shutil
import sys
import unittest

import avro_to_python
from avro_to_python.reader.read import AvscReader
from avro_to_python.utils.paths import get_joined_path
from avro_to_python.writer.writer import AvroWriter


class PathTests(unittest.TestCase):
    def setUp(self):
        """ place empty avsc files in /tmp dir for testing paths """
        self.source = os.path.abspath(avro_to_python.__file__) \
            .replace(get_joined_path('avro_to_python', '__init__.py'), 'tests/avsc/namespace_duplicate_test')
        reader = AvscReader(directory=self.source)
        reader.read()
        writer = AvroWriter(reader.file_tree)

        self.write_path = os.path.abspath(
            self.source.replace(get_joined_path('tests', 'avsc', 'namespace_duplicate_test'), '')
        )

        writer.write(root_dir=self.write_path)
        sys.path.append(self.write_path)

    def test_namespace_duplicate(self):
        if os.path.isdir("tests/avsc/namespace_duplicate_test/test/"):
            shutil.rmtree("tests/avsc/namespace_duplicate_test/test/")
        reader = AvscReader(
            directory=self.source)
        reader.read()
        writer = AvroWriter(
            reader.file_tree,
            pip=None,
            author=None,
            package_version=None
        )
        writer.write(root_dir="tests/avsc/namespace_duplicate_test/test/")
        del reader
        self.assertFalse(
            os.path.isfile("tests/avsc/namespace_duplicate_test/test/namespace_duplicate_test/unique/Common.py")
        )
        self.assertTrue(
            os.path.isfile("tests/avsc/namespace_duplicate_test/test/namespace_duplicate_test/common/enums/CommonEnum.py")
        )
        self.assertTrue(
            os.path.isfile("tests/avsc/namespace_duplicate_test/test/namespace_duplicate_test/unique/UniqueEnum.py")
        )
        self.assertTrue(
            os.path.isfile("tests/avsc/namespace_duplicate_test/test/namespace_duplicate_test/common/TraceContext.py")
        )
        return 0
