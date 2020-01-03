avro-to-python
--------------

avro-to-python is a light tool for compiling avro schema files (.avsc) to python classes making using avro schemata easy.


* Free software: MIT license
* Documentation: https://avro-to-python.readthedocs.io.


Features
--------

* TODO


Roadmap
-------

#### Reader
- [X] Create Namespace Trees on nested namespaces
- [X] Read Record and Enum File
- [X] Primitive types
- [X] Array Types
- [X] Union types
- [X] References to other files
- [ ] Logical Types (Currently just converts to primitive types)

#### Writer
- [X] Base Schema Writer
- [X] Base Record Schema
- [X] Base Enum Schema
- [X] Primitive Types Schema
- [X] Array Types Schema
- [X] Union Types Schema
- [ ] Logical Types Schema (Currently just converts to primitive types)
- [X] Add configs to pip install package

#### CLI
- [X] Wrap Writer and Reader into one cli commant
- [X] Add pip install option (would include all files to pip install compiled package)
- [ ] Add better --help documentation

#### Documentation
- [ ] Document reader class
- [ ] Document writer class
- [ ] Document cli