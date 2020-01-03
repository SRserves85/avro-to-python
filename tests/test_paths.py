""" tests for the reader and reader utils """


import os
import shutil
import unittest

from avro_to_python.utils.paths import (
    get_avsc_files, get_system_path, verify_path_exists, is_avsc_file,
    get_or_create_path, verify_or_create_namespace_path
)


class PathTests(unittest.TestCase):
    def setUp(self):
        """ place empty avsc files in /tmp dir for testing paths """

        # create tmp dir and files for path testing
        os.mkdir('/tmp/avro')
        os.mkdir('/tmp/avro/nest')

        with open('/tmp/avro/test1.avsc', 'w') as f:
            f.write('this is a test file')

        with open('/tmp/avro/nest/test2.avsc', 'w') as f:
            f.write('this is another test file')

        with open('/tmp/avro/nest/bad.txt', 'w') as f:
            f.write('this is not an avsc file')

    def tearDown(self):
        # remove the files we created
        shutil.rmtree('/tmp/avro')

    def test_get_avsc_files(self):
        """ tests that avsc files are read correctly """
        expected = [
            '/tmp/avro/test1.avsc',
            '/tmp/avro/nest/test2.avsc'
        ]

        files = get_avsc_files('/tmp/avro')

        bad_file = '/tmp/avro/nest/bad.txt' not in files

        self.assertEqual(
            expected,
            files,
            'expected values are not the same'
        )

        self.assertTrue(
            bad_file,
            'bad.txt was found in the files!!'
        )

    def test_verify_path_exists(self):
        """ tests that file exists function works """
        should_exist = verify_path_exists('/tmp/avro/nest/test2.avsc')
        should_not_exist = verify_path_exists('/tmp/avro/test2.avsc')
        self.assertTrue(
            should_exist,
            'expected /tmp/avro/nest/test2.avsc to exist'
        )
        self.assertFalse(
            should_not_exist,
            'expected /tmp/avro/test2.avsc to not exist'
        )

    def test_is_avsc_file(self):
        """ test the is_avsc_file function """
        is_avsc = is_avsc_file('/tmp/avro/nest/test2.avsc')
        is_not_avsc = is_avsc_file('/tmp/avro/nest/bad.txt')

        self.assertTrue(
            is_avsc,
            '/tmp/avro/nest/test2.avsc is an avsc file!'
        )
        self.assertFalse(
            is_not_avsc,
            '/tmp/avro/nest/bad.txt is an avsc file!'
        )

    def test_get_system_file_path(self):
        """ tests that you can get the system path of a file """
        expected = '/tmp/avro/nest/test2.avsc'

        # change dir to alter local path
        cwd = os.getcwd()
        os.chdir('/tmp')

        tmp_wd = os.getcwd()

        expected = tmp_wd + '/avro/nest/test2.avsc'

        path1 = get_system_path('avro/nest/test2.avsc')

        # change dir to alter local path
        cwd = os.getcwd()
        os.chdir('/tmp/avro/nest')
        print(os.getcwd())

        path2 = get_system_path('test2.avsc')

        # change back to original dir to prevent errors
        os.chdir(cwd)

        self.assertEqual(
            path1,
            path2,
            f'paths not equal: {path1} != {path2}'
        )

        self.assertEqual(
            expected,
            path2,
            f'paths not equal: {expected} != {path2}'
        )

        def test_verify_or_create_namespace_path(self):
            """ tests that verify_or_create_namespace_path works """
            rootdir = '/tmp'
            namespace = 'test.namespace.path'

            verify_or_create_namespace_path(
                rootdir=rootdir,
                namespace=namespace
            )

            self.assertTrue(
                verify_path_exists('/tmp/test/namespace/path/'),
                'should have created the path from a namespace'
            )

            verify_or_create_namespace_path(
                rootdir=rootdir,
                namespace=namespace
            )

            self.assertTrue(
                verify_path_exists('/tmp/test/namespace/path/'),
                'should have created the path from a namespace'
            )
            os.rmdir('/tmp/test/')

        def test_get_or_create_path(self):
            """ tests that get_or_create_path works """
            path = '/tmp/test'

            get_or_create_path(path=path)

            self.assertTrue(
                verify_path_exists('/tmp/test'),
                'should have created path at /tmp/test'
            )
            os.rmdir(path)

            os.chdir('/tmp')

            get_or_create_path(path='test')

            self.assertTrue(
                verify_path_exists('/tmp/test'),
                'should have created path at /tmp/test from relative path'
            )
            os.rmdir(path)
