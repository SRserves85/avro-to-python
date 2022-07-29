"""Tests for `avro_to_python` package."""

import json
import os
import shutil
import subprocess
import sys
import unittest

from click.testing import CliRunner

import avro_to_python
from avro_to_python import cli
from avro_to_python.utils.paths import get_joined_path


class CliTests(unittest.TestCase):
    def setUp(self):
        """ place empty avsc files in /tmp dir for testing paths """
        self.source = os.path.abspath(avro_to_python.__file__) \
            .replace(get_joined_path('avro_to_python','__init__.py'), 'tests/avsc/records')

    def tearDown(self):
        shutil.rmtree('records', ignore_errors=True)
        shutil.rmtree('test-pip', ignore_errors=True)
        shutil.rmtree('test-top-level-package', ignore_errors=True)

    def test_cli_interface(self):
        """Test the CLI."""
        runner = CliRunner()
        result = runner.invoke(cli.main)
        assert result.exit_code == 2

        help_result = runner.invoke(cli.main, ['--help'])
        assert help_result.exit_code == 0
        assert 'Show this message and exit.' in help_result.output

    def test_pip_cli(self):
        """ tests that the cli can make a non-pip run """
        runner = CliRunner()
        args = [self.source, './', '--pip', 'test-pip']
        result = runner.invoke(cli.main, args)
        assert result.exit_code == 0

        # Install the package using -e for local
        subprocess.check_call(
            [sys.executable, '-m', 'pip', 'install', '-e', './test-pip']
        )

        # when pip installing, it isn't actually added to $PATH
        sys.path.append('test-pip')

        # import a namespace
        from test_pip.records import RecordWithRecord

        data1 = {'thing1': {'id': 10}, 'thing2': {'id': 0}}
        record1 = RecordWithRecord(data1)

        self.assertEqual(
            json.dumps(data1),
            record1.serialize()
        )

        subprocess.check_call(
            [sys.executable, '-m', 'pip', 'uninstall', '-y', 'test-pip']
        )
        del runner

    def test_top_level_package_cli(self):
        """ tests that the cli can make a non-pip run """
        runner = CliRunner()
        args = [self.source, './', '--pip', 'test-top-level-package', '--top_level_package', 'event']
        result = runner.invoke(cli.main, args)
        assert result.exit_code == 0

        # Install the package using -e for local
        subprocess.check_call(
            [sys.executable, '-m', 'pip', 'install', '-e', './test-top-level-package']
        )

        # when pip installing, it isn't actually added to $PATH
        sys.path.append('test-top-level-package')

        # import a namespace
        from event.records import RecordWithRecord

        data1 = {'thing1': {'id': 10}, 'thing2': {'id': 0}}
        record1 = RecordWithRecord(data1)

        self.assertEqual(
            json.dumps(data1),
            record1.serialize()
        )

        subprocess.check_call(
            [sys.executable, '-m', 'pip', 'uninstall', '-y', 'test-top-level-package']
        )
        del runner
