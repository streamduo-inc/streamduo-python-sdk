import json


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