import avro

class Avro:
    schema = None
    """
    Provides methods for validating records and files against a given AVRO schema
    """
    def __init__(self):
        pass


    def set_local_schema(self, schema_file):
        self.schema = avro.schema.parse(open(schema_file, "rb").read())
        print(self.schema)




