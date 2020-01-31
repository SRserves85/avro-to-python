""" base file class for avro file structure """

from typing import List, Union


class File(object):

    name = None
    avrotype = None
    namespace = None
    schema = None
    imports = []
    fields = {}
    enum_sumbols = []

    def __init__(self, name: str, avrotype: str, namespace: str,
                 schema: dict, imports: List[object]=[],
                 fields: List[object]={}, enum_sumbols: List[str]=[]):
        self.name = name
        self.avrotype = avrotype
        self.namespace = namespace
        self.schema = schema
        self.imports = imports
        self.fields = fields

    def __eq__(self, other: Union['File', str]):
        if isinstance(other, File):
            return self.name == other.name
        elif isinstance(other, str):
            return self.name == other

    def __repr__(self):
        return f"<FileObject:'{self.name}'>"
