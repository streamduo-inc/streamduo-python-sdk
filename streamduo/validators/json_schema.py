import json
import csv
from jsonschema import validate, validators


def validate_schema(schema):
    return validators.Draft7Validator.check_schema(schema)


class JsonValidator:
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
                self.set_schema(json.load(file))
        except SyntaxError as error:
            raise

    def set_schema(self, schema):
        self.schema = schema
        print(validators.Draft7Validator.check_schema(self.schema))
        # integer :: int
        # number :: float
        for k, v in self.schema['properties'].items():
            if v['type'] == 'integer':
                self.int_fields.append(k)
            elif v['type'] == 'number':
                self.float_fields.append(k)

    def validate_record(self, record):
        ## retype numerics
        for x in self.int_fields:
            record[x] = int(record[x])
        for y in self.float_fields:
            record[y] = float(record[y])
        return validate(record, self.schema) is None

    def validate_list(self, record_list):
        for r in record_list:
            if not self.validate_record(r):
                return False
        return True

    def validate_csv(self, csv_file_path):
        with open(csv_file_path) as csv_file:
            csv_reader = csv.DictReader(csv_file)
            for r in csv_reader:
                if not self.validate_record(r):
                    return False
        return True
