from unittest import TestCase

import jsonschema

from streamduo.validate import Validator


class TestAvro(TestCase):
    def test_rec_local_schema(self):
        val = Validator()
        val.set_local_schema("unit/car_schema.json")
        valid_rec = {
            "Make": "Nissan",
            "Price": "$9,700.00",
            "Odometer (KM)": "31600",
            "Colour": "White",
            "Doors": "4"
        }
        assert val.validate_record(valid_rec)
        inval_rec = valid_rec['extra'] = "xyz"
        with self.assertRaises(jsonschema.exceptions.ValidationError):
            val.validate_record(inval_rec)

    def test_csv_local_schema(self):
        val = Validator()
        val.set_local_schema("unit/car_schema.json")
        assert val.validate_csv("integration/car_sales.csv")

