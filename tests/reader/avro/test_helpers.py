""" tests helper avro reader functions """

import unittest
from avro_to_python.utils.avro.helpers import (
    _create_reference, _get_namespace
)
from avro_to_python.utils.exceptions import BadReferenceError


class AvroHelperTests(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_reference_creation(self):
        """ tests the _create_reference function """

        # test the function works
        expected = {
            'avro_type': 'reference',
            'name': 'test',
            'namespace': 'test.test'
        }

        created = _create_reference({
            'name': 'test',
            'namespace': 'test.test'
        })

        outcome = expected == created
        self.assertTrue(
            outcome,
            'expected a different reference to be created'
        )

        # test error handling works
        try:
            _ = _create_reference({
                # 'name': 'test',
                'namespace': 'test.test'
            })  # NOQA
        except Exception as e:
            self.assertEqual(
                BadReferenceError,
                e,
                'the error should be a BadReferenceError'
            )

        # test other error handling works
        try:
            _ = _create_reference({
                'name': 'test',
                # 'namespace': 'test.test'
            })
        except Exception as e:
            self.assertEqual(
                BadReferenceError,
                e,
                'the error should be a BadReferenceError'
            )

    def test_namespace_retrieval(self):
        """ tests the _get_namespace helper function works """

        expected = 'test.test'
        empty_expected = ''

        has_namespace = {'namespace': 'test.test'}
        parent_namespace = 'test.test'

        namespace = _get_namespace(has_namespace)
        parent = _get_namespace({}, parent_namespace=parent_namespace)
        empty = _get_namespace({})

        self.assertEqual(
            expected,
            namespace,
            'an object with a namespace should return the namespace'
        )
        self.assertEqual(
            parent_namespace,
            parent,
            'an object with no namespace but a parent_namespace should return the parent_namespace'  # NOQA
        )
        self.assertEqual(
            empty_expected,
            empty,
            'an object with no namespace or parent_namespace should return an empty string'  # NOQA
        )
