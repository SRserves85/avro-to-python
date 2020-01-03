""" tests for the reader and reader utils """

import json
import os
import sys
import unittest

import avro_to_python
from avro_to_python.reader.read import AvscReader
from avro_to_python.writer.writer import AvroWriter


class PathTests(unittest.TestCase):
    def setUp(self):
        """ place empty avsc files in /tmp dir for testing paths """
        directory = os.path.abspath(avro_to_python.__file__) \
            .replace('avro_to_python/__init__.py', 'tests/avsc/records')
        reader = AvscReader(
            directory=directory
        )
        reader.read()
        writer = AvroWriter(reader.file_tree)

        write_path = os.path.abspath('./')
        writer.write(root_dir=write_path)
        sys.path.append(write_path)

    def tearDown(self):
        """ remove all the compiled files"""
        pass

    def test_thing(self):
        """ tests that you can serialize and deserialize thing record """

        from records import Thing

        data = {'id': 10}
        data_json = json.dumps(data)
        thing = Thing(data)
        thing_from_thing = Thing(thing)
        thing_from_json = Thing(data_json)

        self.assertEqual(
            eval(thing.serialize()),
            data,
            'thing should serialize to {"id": 10}'
        )

        self.assertEqual(
            json.dumps(thing.__dict__),
            thing_from_thing.serialize(),
            'thing should be able to serialize itself'
        )

        self.assertEqual(
            thing.serialize(),
            thing_from_json.serialize(),
            'thing should be able to initialize from json'
        )

    def test_record_with_record(self):
        """ tests nested records work """

        from records import RecordWithRecord
        from records import Thing

        data1 = {'thing1': {'id': 10}, 'thing2': {'id': 0}}
        data2 = {'thing1': Thing({'id': 10}), 'thing2': Thing({'id': 0})}
        data_with_default = {'thing1': {'id': 10}}

        record1 = RecordWithRecord(data1)
        record2 = RecordWithRecord(data2)
        record3 = RecordWithRecord(data_with_default)

        self.assertEqual(
            record1.serialize(),
            record2.serialize(),
            'nested records should be equal'
        )

        self.assertEqual(
            record1.serialize(),
            record3.serialize(),
            'records should be equal'
        )

    def test_enum(self):
        """ tests Enums work """

        from records.nested import Flavor

        data = 'CHOCOLATE'
        bad_data = 'MINT'

        flavor = Flavor(data)

        self.assertEqual(
            flavor,
            Flavor(data),
            'enum types should be able to initialize themselves'
        )

        self.assertEqual(
            flavor.serialize(),
            f'''"CHOCOLATE"''',  # JSON serializes single strings this way
            'flavor should serialize to an enum value string'
        )

        with self.assertRaises(ValueError):
            Flavor(bad_data)

    def test_record_with_enum(self):
        """ tests records with nested enums work """

        from records import RecordWithEnum
        from records.nested import Flavor

        data1 = {'favoriteFlavor': 'CHOCOLATE'}
        data2 = {'favoriteFlavor': Flavor('CHOCOLATE')}
        data3 = '{"favoriteFlavor": "CHOCOLATE"}'

        record1 = RecordWithEnum(data1)
        record2 = RecordWithEnum(data2)
        record3 = RecordWithEnum(data3)

        self.assertEqual(
            record1.serialize(),
            record2.serialize()
        )

        self.assertEqual(
            record1.serialize(),
            record3.serialize()
        )

    def test_record_with_logical_types(self):
        """ tests records with logical types work """

        # TODO: Impliment logical types (currently converts to primitives)

        from records import RecordWithLogicalTypes

        data1 = {'timestamp': 100000}
        data2 = {'timestamp': 'not_a_long'}

        record1 = RecordWithLogicalTypes(data1)

        self.assertEqual(
            record1.serialize(),
            json.dumps(data1)
        )

        with self.assertRaises(TypeError):
            RecordWithLogicalTypes(data2)

    def test_record_with_array(self):
        """ tests records with arrays """

        from records import RecordWithArray
        from records import Thing

        data1 = {'things': [{'id': 10}, {'id': 50}], 'numbers': [10, 40]}
        data2 = {'things': [Thing({'id': 10}), {'id': 50}], 'numbers': [10, 40]}  # NOQA
        data3 = {'things': [], 'numbers': []}
        data4 = {'things': [{'id': 10}, {'id': 50}], 'numbers': ['not a long']}
        data5 = {'things': [{'id': 'not a long'}, {'id': 50}], 'numbers': [10, 40]}  # NOQA

        record1 = RecordWithArray(data1)
        record2 = RecordWithArray(data2)
        record3 = RecordWithArray(data3)

        self.assertEqual(
            record1.serialize(),
            record2.serialize(),
            'array records not able to initialize with nested objects'
        )

        self.assertEqual(
            record3.serialize(),
            '{"things": [], "numbers": []}'
        )

        self.assertEqual(
            record1.dict(),
            data1
        )

        with self.assertRaises(TypeError):
            RecordWithArray(data4)

        with self.assertRaises(TypeError):
            RecordWithArray(data5)

    def test_record_with_union(self):
        """ tests records with union types """

        from records import RecordWithUnion
        from records import Thing

        data1 = {'optionalString': 'hello', 'intOrThing': Thing({'id': 2})}
        data2 = {'optionalString': 'hello', 'intOrThing': {'id': 2}}
        data3 = {'optionalString': None, 'intOrThing': 10}
        data4 = {'optionalString': 'hello', 'intOrThing': 'not int or thing'}

        record1 = RecordWithUnion(data1)
        record2 = RecordWithUnion(data2)
        record3 = RecordWithUnion(data3)

        self.assertEqual(
            '{"optionalString": "hello", "intOrThing": {"id": 2}}',
            record1.serialize()
        )

        self.assertEqual(
            record1.serialize(),
            record2.serialize()
        )

        self.assertEqual(
            record3.__dict__,
            {'optionalString': None, 'intOrThing': 10}
        )

        self.assertEqual(
            record3.serialize(),
            '{"optionalString": null, "intOrThing": 10}'
        )

        with self.assertRaises(TypeError):
            RecordWithUnion(data4)
