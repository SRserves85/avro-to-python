""" tests for the reader and reader utils """

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
            .replace(get_joined_path('avro_to_python', '__init__.py'), 'tests/avsc/records')
        reader = AvscReader(directory=self.source)
        reader.read()
        writer = AvroWriter(reader.file_tree)

        self.write_path = os.path.abspath(
            self.source.replace(get_joined_path('tests', 'avsc', 'records'), '')
        )

        writer.write(root_dir=self.write_path)
        sys.path.append(self.write_path)

    def tearDown(self):
        """ remove all the compiled files"""
        shutil.rmtree(self.write_path + '/records')

    def test_escape_chars(self):
        """ tests that escape characters are not lost """

        from records import EscapedChars
        schema = r"""
    {
        "type": "record",
        "name": "EscapedChars",
        "namespace": "records",
        "doc": "This is an example \"schema\".",
        "fields": [
            {
                "name": "name",
                "type": "string"
            }
        ]
    }
    """

        self.assertEqual(
            schema,
            EscapedChars.schema,
            "Schema should contain escape characters"
        )

    def test_thing(self):
        """ tests that you can serialize and deserialize thing record """

        from records import Thing

        data = {'id': 10}
        data_json = json.dumps(data)
        thing = Thing(data)
        thing_from_thing = Thing(thing)
        thing_from_json = Thing(data_json)
        thing_from_setters = Thing()
        thing_from_setters.id = 10

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

        self.assertEqual(
            thing.serialize(),
            thing_from_setters.serialize(),
            'thing should be able to initialize from setters'
        )

    def test_record_with_numbers(self):
        """ tests records with numbers work """

        from records import RecordWithNumbers

        data1 = {'booleanValue': True, 'nullableBooleanValue': None, 'intValue': 3, 'longValue': 4000000000,
                 'floatValue': 1.234E3, 'nullableFloatValue': None, 'doubleValue': 1.234567890123456789E18}
        data2 = ('{"booleanValue": true, "nullableBooleanValue": null, "intValue": 3, "longValue": 4000000000, '
                 '"floatValue": 1.234E3, "nullableFloatValue": null, '
                 '"doubleValue": 1.2345678901234567E18}')
        data3 = ('{"booleanValue": true, "intValue": 3, "longValue": 4000000000, '
                 '"floatValue": 1234,'
                 '"doubleValue": 1234567890123456789}')

        record1 = RecordWithNumbers(data1)
        record2 = RecordWithNumbers(data2)
        record3 = RecordWithNumbers(data3)

        self.assertEqual(
            record1.serialize(),
            record2.serialize(),
            'records should be equal'
        )

        self.assertEqual(
            record1.serialize(),
            record3.serialize(),
            'records should be equal'
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

    def test_record_with_circular_reference(self):
        """ tests records with circular references """

        from records import RecordWithCircularReference
        from records import Node
        import records.nested.Node

        data1 = {'tree': {'id': '0',
                          'children': [Node({'id': '00', 'parent': Node({'id': '0'})}),
                                       {'id': '01', 'parent': {'id': '0'},
                                        'children': [{'id': '010', 'parent': Node({'id': '01'})},
                                                     {'id': '011',
                                                      'parent': Node({'id': '01'})}]}]},
                 'altTree': records.nested.Node({'name': 'x'})}
        data2 = ('{"tree": {"id": "0", "children": [{"id": "00", "parent": {"id": "0"}}, '
                 '{"id": "01", "parent": {"id": "0"}, "children": [{"id": "010", "parent": {"id": "01"}}, '
                 '{"id": "011", "parent": {"id": "01"}}]}]}, "altTree": {"name": "x"}}')

        record1 = RecordWithCircularReference(data1)
        record2 = RecordWithCircularReference(data2)

        self.assertEqual(
            record1.serialize(),
            record2.serialize(),
            'records with circular references should be equal'
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

    def test_record_with_bytes(self):
        """ tests records with bytes work """

        from records import RecordWithBytes

        data1 = '{"binaryData": "SGVsbG8gd29ybGQh"}'
        data2 = {'binaryData': b"Hello world!"}

        record1 = RecordWithBytes(data1)
        record2 = RecordWithBytes(data2)
        record3 = RecordWithBytes()
        record3.binaryData = b"Hello world!"

        self.assertEqual(
            record1.serialize(),
            data1
        )

        self.assertEqual(
            record1.serialize(),
            record2.serialize()
        )

        self.assertEqual(
            record1.binaryData,
            record2.binaryData
        )

        self.assertEqual(
            record1.serialize(),
            record3.serialize()
        )

        self.assertEqual(
            record1.binaryData,
            record3.binaryData
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

        data1 = {'things': [{'id': 10}, {'id': 50}], 'numbers': [10, 40], 'things2': [],
                 'twoDimDoubleArray': [[1.1, 2.2], [3.3, 4.5]], 'threeDimRecordArray': [[[{'id': 10}, {'id': 50}]]],
                 'arrayOfUnion': [7, {'id': 8}]}  # NOQA
        data2 = {'things': [Thing({'id': 10}), {'id': 50}], 'numbers': [10, 40], 'things2': [],
                 'twoDimDoubleArray': [[1.1, 2.2], [3.3, 4.5]],
                 'threeDimRecordArray': [[[Thing({'id': 10}), {'id': 50}]]],
                 'arrayOfUnion': [7, Thing({'id': 8})]}  # NOQA
        data3 = {'things': [], 'numbers': [], 'things2': [], 'twoDimDoubleArray': [], 'threeDimRecordArray': [],
                 'arrayOfUnion': []}  # NOQA
        data4 = {'things': [{'id': 10}, {'id': 50}], 'numbers': ['not a long'], 'things2': [],
                 'arrayOfUnion': []}  # NOQA
        data5 = {'things': [{'id': 'not a long'}, {'id': 50}], 'numbers': [10, 40], 'things2': [],
                 'arrayOfUnion': []}  # NOQA

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
            '{"things": [], "numbers": [], "things2": [], "twoDimDoubleArray": [], "threeDimRecordArray": [], '
            '"arrayOfUnion": []}'
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
        from records.nested import Flavor

        data1 = {'optionalString': 'hello', 'intOrThing': Thing({'id': 2}), 'nullOrThingArray': None,
                 'nullOrEnum': Flavor('CHOCOLATE')}
        data2 = {'optionalString': 'hello', 'intOrThing': {'id': 2}, 'nullOrEnum': 'CHOCOLATE'}
        data3 = {'optionalString': None, 'intOrThing': 10, 'nullOrThingArray': [{'id': 2}], 'nullOrMap': {'value': 0.1}}
        data4 = {'optionalString': 'hello', 'intOrThing': 'not int or thing'}

        record1 = RecordWithUnion(data1)
        record2 = RecordWithUnion(data2)
        record3 = RecordWithUnion(data3)

        self.assertEqual(
            '{"optionalString": "hello", "intOrThing": {"id": 2}, "nullOrThingArray": null, "nullOrMap": null, '
            '"nullOrEnum": "CHOCOLATE"}',
            record1.serialize()
        )

        self.assertEqual(
            record1.serialize(),
            record2.serialize()
        )

        self.assertEqual(
            record3.nullOrThingArray[0].id,
            2
        )

        self.assertEqual(
            record3.optionalString,
            None
        )

        self.assertEqual(
            record3.intOrThing,
            10
        )

        self.assertEqual(
            record3.serialize(),
            '{"optionalString": null, "intOrThing": 10, "nullOrThingArray": [{"id": 2}], '
            '"nullOrMap": {"value": 0.1}, "nullOrEnum": null}'
        )

        with self.assertRaises(TypeError):
            RecordWithUnion(data4)

    def test_record_with_geometries(self):
        """ tests records with union types """

        from records import RecordWithGeometries
        from records import Point
        from records import LineString
        from records import Thing

        data1 = {'geometries': None}
        data2 = {'geometries': [
            LineString({"bbox": None, "coordinates": [[-96.41675, 33.968745], [-96.416745, 33.96757]],
                        "type": "LineString"}),
            Point({"bbox": None, "coordinates": [-96.41675, 33.968745], "type": "Point"})]}
        data3 = {'geometries': [
            {"bbox": None, "coordinates": [[-96.41675, 33.968745], [-96.416745, 33.96757]], "type": "LineString"},
            {"bbox": None, "coordinates": [-96.41675, 33.968745], "type": "Point"}]}
        data4 = {'geometries': [Thing({"id": 1})]}

        record1 = RecordWithGeometries(data1)
        record2 = RecordWithGeometries(data2)
        record3 = RecordWithGeometries(data3)
        record4 = RecordWithGeometries(data4)

        self.assertEqual(
            '{"geometries": null}',
            record1.serialize()
        )

        self.assertEqual(
            record2.serialize(),
            record3.serialize()
        )

        self.assertEqual(
            record2.serialize(),
            '{"geometries": [{"bbox": null, "coordinates": [[-96.41675, 33.968745], [-96.416745, 33.96757]], '
            '"type": "LineString"}, {"bbox": null, "coordinates": [-96.41675, 33.968745], "type": "Point"}]}'
        )

        self.assertIsInstance(
            record3.geometries[0],
            LineString
        )

        self.assertIsInstance(
            record3.geometries[1],
            Point
        )

        self.assertEqual(
            len(record4.geometries),
            0
        )

    def test_nested_things(self):
        """ tests that nested things have correct mappings and namespaces """

        from records.nested import Thing2, Thing3

        data1 = {'chars': 'this is a string'}
        data2 = {}
        data3 = {'chars': 10}

        record1 = Thing2(data1)
        record2 = Thing3(data2)

        with self.assertRaises(TypeError):
            Thing2(data2)

        with self.assertRaises(TypeError):
            Thing3(data3)

        with self.assertRaises(TypeError):
            Thing2(data2)

        self.assertEqual(
            record1.dict(),
            data1
        )

        self.assertEqual(
            record2.chars,
            'string default'
        )

    def test_map_record(self):
        """ tests that nested things have correct mappings and namespaces """

        from records import RecordWithMap
        from records import Thing

        data1 = {'thingMap': {'string1': {'id': 10},
                              'string2': Thing({'id': 10})},
                 'intMap': {'lksdfl': 23},
                 'thingMap2': {'string1': {'id': 10},
                               'string2': Thing({'id': 10})},
                 'thingMap3': {'string1': {'id': 10},
                               'string2': Thing({'id': 10})},
                 'arrayMap': {'string1': ['value1', 'value2']},
                 'arrayOfUnionMap': {
                     'string1': [Thing({'id': 10}), None]
                 }
                 }
        data2 = {'thingMap': {'string1': {'id': 10},
                              'string2': Thing({'id': 10})},
                 'intMap': {'lksdfl': 'NOT A STRING'}}
        data3 = {'thingMap': [{'string1': {'id': 10}},
                              {'string2': Thing({'id': 10})}],
                 'intMap': [{'lksdfl': 23}]}

        record1 = RecordWithMap(data1)
        record2 = RecordWithMap(record1)

        with self.assertRaises(TypeError):
            RecordWithMap(data2)

        with self.assertRaises(TypeError):
            RecordWithMap(data3)

        self.assertEqual(
            record1.serialize(),
            record2.serialize()
        )

    def test_nested_map_record(self):
        """ tests that nested maps will work """

        from records import RecordWithNestedMap
        from records import Thing

        data1 = {
            'thingMap': {
                'string1': {'id': 10},
                'string2': Thing({'id': 10})
            },
            'nestedThingMap': {
                'foo': {
                    'string1': {'id': 10},
                    'string2': Thing({'id': 10})
                },
                'bar': {
                    'string1': {'id': 10},
                    'string2': Thing({'id': 10})
                },
            },
            'nestedIntMap': {
                'foo': {
                    'string1': 10,
                    'string2': 11
                },
                'bar': {
                    'string1': 10,
                    'string2': 11
                },
            },
            'mappedThingArray': {
                'foo': [
                    {'id': 10},
                    Thing({'id': 20})
                ],
                'bar': [
                    {'id': 10},
                    Thing({'id': 20})
                ]
            }
        }

        serialized_data1 = ('{"thingMap": {"string1": {"id": 10}, "string2": {"id": 10}}, "nestedThingMap": '
                            '{"foo": {"string1": {"id": 10}, "string2": {"id": 10}}, "bar": {"string1": {"id": 10}, '
                            '"string2": {"id": 10}}}, "nestedIntMap": {"foo": {"string1": 10, "string2": 11}, "bar": '
                            '{"string1": 10, "string2": 11}}, "mappedThingArray": {"foo": [{"id": 10}, {"id": 20}], '
                            '"bar": [{"id": 10}, {"id": 20}]}}')

        data2 = {
            'thingMap': {
                'string1': {'id': 10},
                'string2': Thing({'id': 10})
            },
            'nestedThingMap': {
                'foo': {
                    'string1': {'id': 10},
                    'string2': Thing({'id': 10})
                },
                'bar': {
                    'string1': {'id': 10},
                    'string2': Thing({'id': 10})
                },
            },
            'nestedIntMap': {
                'foo': {
                    'string1': 'NOT AN INT',
                    'string2': 11
                },
                'bar': {
                    'string1': 10,
                    'string2': 11
                }
            },
            'mappedThingArray': {
                'foo': [
                    {'id': 10},
                    Thing({'id': 20})
                ],
                'bar': [
                    {'id': 10},
                    Thing({'id': 20})
                ]
            }
        }

        record1 = RecordWithNestedMap(data1)
        record2 = RecordWithNestedMap(record1)

        with self.assertRaises(TypeError):
            RecordWithNestedMap(data2)

        self.assertEqual(
            record1.serialize(),
            record2.serialize()
        )

        self.assertEqual(
            serialized_data1,
            record1.serialize(),
        )
