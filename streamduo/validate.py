import json
import csv
from jsonschema import validate, validators

class Validator:
    schema = None
    """
    Provides methods for validating records and files against a given AVRO schema
    """
    def __init__(self):
        pass

    def set_local_schema(self, schema_file):
        try:
            with open(schema_file, 'r') as file:
                self.schema = json.load(file)
                print(validators.Draft7Validator.check_schema(self.schema))
        except SyntaxError as error:
            raise
        print(self.schema)

    def validate_record(self, record):
        return validate(record, self.schema) == None

    def validate_csv(self, csv_file_path):
        with open(csv_file_path) as csv_file:
            csv_reader = csv.DictReader(csv_file)
            for r in csv_reader:
                if not self.validate_record(r):
                    return False
        return True









