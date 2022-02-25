from frictionless import Schema, validate, validate_resource
import json
schema = Schema()
import pprint as pp



def validate_schema(schema):
    with open(schema, 'r') as file:
        schema_obj = json.load(file)
    s = validate_resource(schema_obj)
    pp.pprint(s)

class FrictionValidator:
    schema = None

    def __init__(self):
        pass

    def set_schema(self, schema_path):
        with open(schema_path, 'r') as file:
            self.schema = json.load(file)

    def validate_csv(self, csv_path):
        temp_schema = self.schema.copy()
        temp_schema['path'] = csv_path
        validation_results = validate_resource(temp_schema)
        return validation_results
