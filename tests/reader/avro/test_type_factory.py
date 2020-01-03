""" tests for the type factury function """

import unittest

from avro_to_python.utils.avro.types.type_factory import _get_field_type
from avro_to_python.utils.avro.primitive_types import PRIMITIVE_TYPES


class TestTypeFactory(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_array_field(self):
        """ tests array fields return array type """
        array = {
            'type': {
                'type': 'array'
            }
        }
        not_array = {
            'type': 'record'
        }
        also_not_array = {
            'type': ['this', 'is', 'a', 'union']
        }

        self.assertEqual(
            'array',
            _get_field_type(array),
            'field type should return array'
        )
        self.assertNotEqual(
            'array',
            _get_field_type(not_array),
            'field type should not return array'
        )
        self.assertNotEqual(
            'array',
            _get_field_type(also_not_array),
            'field type shoudl not return array'
        )

    def test_record_type(self):
        """ tests record types return record """
        record = {
            'type': {
                'type': 'record'
            }
        }
        also_record = {
            'type': 'record'
        }
        array = {
            'type': {
                'type': 'array'
            }
        }
        self.assertEqual(
            'record',
            _get_field_type(record),
        )
        self.assertEqual(
            'record',
            _get_field_type(also_record)
        )
        self.assertNotEqual(
            'record',
            _get_field_type(array)
        )

    def test_union_type(self):
        """ tests union types return union """
        union = {
            'type': ['this is a union', 'yay']
        }
        array = {
            'type': {
                'type': 'array'
            }
        }
        self.assertEqual(
            'union',
            _get_field_type(union)
        )
        self.assertNotEqual(
            'union',
            _get_field_type(array)
        )

    def test_enum_type(self):
        """ tests enum types return enum """
        enum = {
            'type': 'enum'
        }
        also_enum = {
            'type': {
                'type': 'enum'
            }
        }
        array = {
            'type': {
                'type': 'array'
            }
        }
        self.assertEqual(
            'enum',
            _get_field_type(enum)
        )
        self.assertEqual(
            'enum',
            _get_field_type(also_enum)
        )
        self.assertNotEqual(
            'enum',
            _get_field_type(array)
        )

    def test_primitive_type(self):
        """ tests primitive types """
        for _type in PRIMITIVE_TYPES:
            primitive = {
                'type': _type
            }
            self.assertEqual(
                'primitive',
                _get_field_type(primitive)
            )
        array = {
            'type': {
                'type': 'array'
            }
        }
        self.assertNotEqual(
            'primitive',
            _get_field_type(array)
        )
