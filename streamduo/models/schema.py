import json
from enum import Enum


class SchemaType(Enum):
    JSON = 'JSON'
    AVRO = 'AVRO'
    GREAT_EXPECTATIONS = 'GREAT_EXPECTATIONS'


class FileType(Enum):
    JSON = 'JSON'
    AVRO = 'AVRO'
    CSV = 'CSV'


class Schema:
    """
    Class used to aid in the use of schema objects
    """

    def __init__(self, **entries):
        self.__dict__.update(entries)

    def to_json(self):
        return self.__dict__

    def get_schema(self):
        return json.loads(self.schema)

    def get_schema_type(self):
        return SchemaType[self.schemaType]
