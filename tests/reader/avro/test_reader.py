""" class to test reading of various avro formats """

import os
import unittest

import avro_to_python
from avro_to_python.reader.read import AvscReader


class AvroReaderTests(unittest.TestCase):

    directory = os.path.abspath(avro_to_python.__file__) \
        .replace('avro_to_python/__init__.py', 'tests/avsc/records')

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testReadThing(self):
        filepath = self.directory + '/Thing.avsc'

        reader = AvscReader(file=filepath)
        reader.read()

        # test node tree structure is correct
        obj = reader.file_tree
        self.assertEqual(
            obj.name,
            ''
        )

        self.assertEqual(
            list(obj.children.keys()),
            ['records']
        )

        # test Thing file is in correct place
        self.assertEqual(
            obj.children['records'].files['Thing'].name,
            'Thing'
        )

        # test Thing.id exists and only once
        self.assertEqual(
            len(obj.children['records'].files['Thing'].fields),
            1
        )

        # test thing.id field has necessary information
        self.assertEqual(
            obj.children['records'].files['Thing'].fields['id'].avrotype,
            'int'
        )

    def testReadRecordWithRecord(self):
        filepath = self.directory + '/RecordWithRecord.avsc'

        reader = AvscReader(file=filepath)
        reader.read()

        # TestReadThing tests from earlier since Thing is same schema
        obj = reader.file_tree
        self.assertEqual(
            obj.name,
            ''
        )

        self.assertEqual(
            list(obj.children.keys()),
            ['records']
        )

        self.assertEqual(
            obj.children['records'].files['Thing'].name,
            'Thing'
        )

        self.assertEqual(
            len(obj.children['records'].files['Thing'].fields),
            1
        )

        self.assertEqual(
            obj.children['records'].files['Thing'].fields['id'].name,
            'id'
        )

        self.assertEqual(
            obj.children['records'].files['Thing'].fields['id'].fieldtype,
            'primitive'
        )

        self.assertEqual(
            obj.children['records'].files['Thing'].fields['id'].avrotype,
            'int'
        )

        # Record with Record has 2 fields
        self.assertEqual(
            len(obj.children['records'].files['RecordWithRecord'].fields),
            2
        )

        # Should have 1 import
        self.assertEqual(
            len(obj.children['records'].files['RecordWithRecord'].imports),
            1
        )

        # import should have correct namespace
        self.assertEqual(
            {'name': 'Thing', 'namespace': 'records'},
            obj.children['records'].files['RecordWithRecord'].imports[0].__dict__  # NOQA
        )

        # make sure thing2 field has a default
        self.assertEqual(
            obj.children['records'].files['RecordWithRecord'].fields['thing2'].default,  # NOQA
            {'id': 0}
        )

        # make sure thing1 field has no default
        self.assertEqual(
            obj.children['records'].files['RecordWithRecord'].fields['thing1'].default,  # NOQA
            None
        )

    def testReadRecordWithEnum(self):
        filepath = self.directory + '/RecordWithEnum.avsc'

        reader = AvscReader(file=filepath)
        reader.read()

        # TestReadThing tests from earlier since Thing is same schema
        obj = reader.file_tree

        # test the enum was created
        flavor_dict = {
            'name': 'Flavor',
            'avrotype': 'enum',
            'namespace': 'records.nested',
            'schema': {
                'type': 'enum',
                'name': 'Flavor',
                'namespace': 'records.nested',
                'symbols': ['VANILLA', 'CHOCOLATE', 'STRAWBERRY']
            },
            'imports': [],
            'fields': {},
            'symbols': ['VANILLA', 'CHOCOLATE', 'STRAWBERRY'],
            'default': None
        }
        self.assertEqual(
            obj.children['records'].children['nested'].files['Flavor'].__dict__,  # NOQA
            flavor_dict
        )

        # test the record referencing enum was created
        self.assertEqual(
            'RecordWithEnum',
            obj.children['records'].files['RecordWithEnum'].name
        )

        # test the RecordWithEnum imports are correct
        self.assertEqual(
            {'name': 'Flavor', 'namespace': 'records.nested'},
            obj.children['records'].files['RecordWithEnum'].imports[0].__dict__
        )

        # test Enum has good symbols
        self.assertEqual(
            ['VANILLA', 'CHOCOLATE', 'STRAWBERRY'],
            obj.children['records'].children['nested'].files['Flavor'].symbols
        )

    def testLogicalRecord(self):
        filepath = self.directory + '/RecordWithLogicalTypes.avsc'

        reader = AvscReader(file=filepath)
        reader.read()

        # TestReadThing tests from earlier since Thing is same schema
        obj = reader.file_tree

        # test logical type was mapped to primitive
        self.assertEqual(
            obj.children['records'].files['RecordWithLogicalTypes'].fields['timestamp'].fieldtype,  # NOQA
            'primitive'
        )

    def testUnionRecord(self):
        filepath = self.directory + '/RecordWithUnion.avsc'

        reader = AvscReader(file=filepath)
        reader.read()

        # TestReadThing tests from earlier since Thing is same schema
        obj = reader.file_tree

        # test both union types have 2 possible fields
        self.assertEqual(
            len(obj.children['records'].files['RecordWithUnion'].fields['optionalString'].union_types),  # NOQA
            len(obj.children['records'].files['RecordWithUnion'].fields['intOrThing'].union_types)  # NOQA
        )

        # test the unions are correct type
        self.assertEqual(
            obj.children['records'].files['RecordWithUnion'].fields['optionalString'].union_types[0].avrotype,  # NOQA
            'string'
        )

        self.assertEqual(
            obj.children['records'].files['RecordWithUnion'].fields['optionalString'].union_types[1].avrotype,  # NOQA
            'null'
        )

        self.assertEqual(
            obj.children['records'].files['RecordWithUnion'].fields['intOrThing'].union_types[0].avrotype,  # NOQA
            'int'
        )

        self.assertEqual(
            obj.children['records'].files['RecordWithUnion'].fields['intOrThing'].union_types[1].fieldtype,  # NOQA
            'reference'
        )

        # make sure the import is valid
        self.assertEqual(
            obj.children['records'].files['RecordWithUnion'].imports[0].name,
            'Thing'
        )

    def testRecordWithArray(self):
        filepath = self.directory + '/RecordWithArray.avsc'

        reader = AvscReader(file=filepath)
        reader.read()

        # TestReadThing tests from earlier since Thing is same schema
        obj = reader.file_tree

        # should have 3 fields
        self.assertEqual(
            len(obj.children['records'].files['RecordWithArray'].fields),
            3
        )

        # field 0 should be of type reference
        self.assertEqual(
            obj.children['records'].files['RecordWithArray'].fields['things'].array_item_type.fieldtype,  # NOQA
            'reference'
        )

        # field 1 should be of type primitive
        self.assertEqual(
            obj.children['records'].files['RecordWithArray'].fields['numbers'].array_item_type.fieldtype,  # NOQA
            'primitive'
        )

        # field 2 should be of type reference
        self.assertEqual(
            obj.children['records'].files['RecordWithArray'].fields['things2'].array_item_type.fieldtype,  # NOQA
            'reference'
        )

    def testRecordWithMap(self):
        filepath = self.directory + '/RecordWithMap.avsc'

        reader = AvscReader(file=filepath)
        reader.read()

        # TestReadThing tests from earlier since Thing is same schema
        obj = reader.file_tree

        # should have 1 field
        self.assertEqual(
            len(obj.children['records'].files['RecordWithMap'].fields),
            4
        )

        # field should be of type map
        self.assertEqual(
            obj.children['records'].files['RecordWithMap'].fields['thingMap'].fieldtype,  # NOQA
            'map'
        )

        # thingmap field should be of type Thing
        self.assertEqual(
            obj.children['records'].files['RecordWithMap'].fields['thingMap'].map_type.reference_name,  # NOQA
            'Thing'
        )

        # map int field should be of type Thing
        self.assertEqual(
            obj.children['records'].files['RecordWithMap'].fields['intMap'].map_type.avrotype,  # NOQA
            'int'
        )

    def testRecordWithNestedMap(self):
        filepath = self.directory + '/RecordWithNestedMap.avsc'

        reader = AvscReader(file=filepath)
        reader.read()

        # test parsing works for nested maps
        obj = reader.file_tree
        file = obj.children['records'].files['RecordWithNestedMap']

        self.assertEqual(
            len(obj.children['records'].files['RecordWithNestedMap'].fields),
            4
        )

        # assert reader picked up the nested map
        self.assertEqual(
            file.fields['nestedThingMap'].map_type.map_type.name,
            'Thing'
        )
        self.assertEqual(
            file.fields['nestedThingMap'].map_type.map_type.fieldtype,
            'reference'
        )

        # assert reader picked up nested array in map
        self.assertEqual(
            file.fields['mappedThingArray'].map_type.array_item_type.name,
            'Thing'
        )

        self.assertEqual(
            file.fields['mappedThingArray'].map_type.array_item_type.fieldtype,
            'reference'
        )
