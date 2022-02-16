import json
import csv
from fastavro.validation import validate
from fastavro import parse_schema


def validate_schema(schema):
    parsed_schema = parse_schema(schema)


class AvroValidator:
    schema = None
    int_fields = []
    float_fields = []
    """
    Provides methods for validating records and files against a given AVRO schema
    """

    def __init__(self):
        pass

    def set_local_schema(self, schema_file):
        try:
            with open(schema_file, 'r') as file:
                self.schema = parse_schema(json.load(file))
                print(self.schema)
                # integer :: int
                # number :: float
                for v in self.schema['fields']:
                    if 'long' in v['type'] or 'int' in v['type']:
                        self.int_fields.append(v['name'])
                    elif 'float' in v['type'] or 'double' in v['type']:
                        self.float_fields.append(v['name'])
        except SyntaxError as error:
            raise

    def set_schema(self, schema):
        self.schema = parse_schema(schema)
        print(self.schema)

    def validate_record(self, record):
        ## retype numerics
        try:
            for x in self.int_fields:
                record[x] = int(record[x])
            for y in self.float_fields:
                record[y] = float(record[y])
        except:
            pass
        return validate(record, self.schema)
