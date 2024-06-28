""" base file class for avro file structure """
import copy
from typing import List, Union

from avro_to_python.classes.field import Field
from avro_to_python.classes.reference import Reference


class File(object):
    name = None
    avrotype = None
    namespace = None
    schema = None
    imports = []
    fields = {}
    enum_sumbols = []

    def __init__(self, name: str, avrotype: str, namespace: str,
                 schema: dict, imports: List[object] = [],
                 fields: List[object] = {}, enum_sumbols: List[str] = []):
        self.name = name
        self.avrotype = avrotype
        self.namespace = namespace
        self.schema = schema
        self.orig_schema = copy.deepcopy(schema)
        self.imports = imports
        self.aliased_imports = []
        self.fields = fields

    def __eq__(self, other: Union['File', str]):
        if isinstance(other, File):
            return self.name == other.name
        elif isinstance(other, str):
            return self.name == other

    def __repr__(self):
        return f"<FileObject:'{self.name}'>"

    def resolve_reference_name(self, field: Field, pip_import_prefix: str, is_method: bool = False):
        ref = Reference(field.reference_name, field.reference_namespace)
        is_circular_ref = False
        has_name_clash = False

        if field.reference_name == self.name:
            if field.reference_namespace == self.namespace:
                # Circular reference. It must be quoted in method declaration
                is_circular_ref = True
            else:
                # Name clash. Complete reference name must be returned
                has_name_clash = True
        elif ref in self.aliased_imports:
            has_name_clash = True

        if is_circular_ref and is_method:
            ref_name = f"'{ref.name}'"
        elif has_name_clash:
            ref_name = f"{pip_import_prefix.replace('.','_')}{ref.namespace.replace('.','_')}_{ref.name}"
        else:
            ref_name = ref.name

        return ref_name
