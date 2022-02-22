===============================
avro-to-python AvscReader Logic
===============================

Overview
^^^^^^^^
``AvscReader`` class calls ``.read()`` to accomplish the following two things:

* read and serialize .avsc file into JSON object and append it to a list stored in the reader
* build a namespace tree where each node in the tree has a name, a dictionary of file objects, and a dictionary of children nodes
    * each node represents a namespace; in the ``RecordWithNestedUnion`` test example, the namespace tree that is ultimately built consists of a root node, a child of the root node named ``records``, and a child of ``records`` named ``nested``

Once the namespace tree has been built, it is passed to the ``AvroWriter`` class. This class traverses the tree and writes the information in each node's file objects to Python files as Python classes.

Building Namespace Tree From .avsc Files with AvscReader
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
* ``AvscReader`` is given an .avsc file to parse. Below is an example of the contents of ``RecordWithNestedUnion.avsc``

.. code-block:: python

    {"type": "record", "name": "RecordWithNestedUnion", "namespace": "records", "fields": [
        {"name": "nestedUnion", "type": ["null",
            {"type": "record", "name": "NestedUnion", "namespace": "records.nested", "fields": [
                {"name": "categories", "type": ["null",
                    {"type": "array", "items": {"type": "record", "name": "CommonReference", "fields": [
                          {"name": "group", "type": "int"},
                          {"name": "isApproved", "type": ["null", "boolean"],
                            "default": null
                          },
                          {"name": "index", "type": ["null", "int"]}
                        ]
                      }
                    }
                  ],
                  "default": null
                }
              ] 
            }
          ],
          "default": null
        },
        {"name": "nestedUnion2", "type": ["null",
           {"type": "record", "name": "NestedUnion2", "namespace": "records.nested", "fields": [
                {"name": "categories2", "type": ["null",
                    {
                     "type": "array",
                     "items": "CommonReference"
                    }
                  ],
                  "default": null
                }
              ]
            }
          ],
          "default": null
        }
      ]
    }

* Each element of type ``record`` or ``enum`` in the .avsc file has its own .avsc file associated with it. Therefore, each element of type ``record`` or ``enum`` will generate a Python fie and needs to be added as a file object to one of he nodes in the namespace tree
* ``AvscReader`` creates these files in a Breadth-First Search order
    * in the example above, ``AvscReader`` creates the file objects for ``RecordWithNestedUnion``, ``NestedUnion``, ``NestedUnion2``, and ``CommonReference`` in that order 
* As ``AvscReader`` traverses through each element in the file, it will add each record it comes across into a ``queue`` to be processed later
    * ``queue`` is initially populated with whatever was serialized by ``AvscReader``. In the case of the above example, the ``queue`` is initially populated with ``RecordWithNestedUnion``
* In general, the overall flow of building the namespace tree is as follows:
    * create empty ``root_node``
    * populate ``queue``
    * until ``queue`` is empty:
        * grab the first ``item`` in the ``queue``
        * get the ``namespace`` of the ``item``
        * create or set ``current_node`` to ``namespace``
        * create skeleton ``file`` for the ``item``
        * if ``item`` is a record
            * traverse its ``fields``
            * for each ``field`` in ``fields``
                * get ``type`` of ``field``
                    * get ``type`` of nested elements if needed (for arrays, unions, etc.)
                    * create that nested element if necessary
                * create that ``field``
                * add the ``field`` to ``file``
                * if ``field`` was a record, add it to the ``queue``
        * if ``item`` is an enum
            * add enum symbols to ``file``
        * add ``file`` to ``current_node``
    * set ``file_tree`` attribute in ``AvscReader`` to ``root_node``
* The resulting namespace tree after reading ``RecordWithNestedUnion.avsc`` is structured as follows:
    * root_node
        * name=''
        * files={}
        * children={Node<'records'>}
    * records
        * name='records'
        * files={File<'RecordWithNestedUnion'>}
        * children={Node<'nested'>}
    * nested
        * name='nested'
        * files={File<'NestedUnion'>, File<'NestedUnion2'>, File<'CommonReference'>}
        * children={}

Additional Notes and Insights
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

* the current node represents the ``namespace`` or directory of the .avsc file
* the ``File`` class represents the contents and meta information of the .avsc file
* the ``item`` in the ``queue`` is the contents of an individual .avsc file
    * everything that gets added to the ``queue`` will have a Python file created for it
* ``get_field_type`` identifies the type of the element being parsed (str, arrays, unions, etc.)
