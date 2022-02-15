from unittest import TestCase
from streamduo.validators.json_schema import Avro


class TestAvro(TestCase):
    def test_set_local_schema(self):
        val = Avro()
        val.set_local_schema("car_schema.avsc")
        print(val.schema)
