from unittest import TestCase

import jsonschema

from streamduo.validators.json_schema import JsonValidator


class TestJson(TestCase):

    def test_json_record_validation(self):
        val = JsonValidator()
        val.set_local_schema("../test_schemas/car_schema.json")
        valid_rec = {
            "Make": "Nissan",
            "Price": "$9,700.00",
            "Odometer (KM)": "31600",
            "Colour": "White",
            "Doors": "4"
        }
        assert val.validate_record(valid_rec)
        inval_rec = valid_rec.copy()
        inval_rec['extra'] = "xyz"
        with self.assertRaises(jsonschema.exceptions.ValidationError):
            val.validate_record(inval_rec)

    def test_json_list_validation(self):
        val = JsonValidator()
        val.set_local_schema("../test_schemas/car_schema.json")
        valid_rec_1 = {
            "Make": "Nissan",
            "Price": "$9,700.00",
            "Odometer (KM)": "31600",
            "Colour": "White",
            "Doors": "4"
        }
        valid_rec_2 = {
            "Make": "Honda",
            "Price": "$9,700.00",
            "Odometer (KM)": "31600",
            "Colour": "White",
            "Doors": "4"
        }
        rec_list = [valid_rec_1, valid_rec_2]
        assert val.validate_list(rec_list)

        ## Make Bad
        rec_list[1]['extra'] = "xyz"
        with self.assertRaises(jsonschema.exceptions.ValidationError):
            val.validate_list(rec_list)

    def test_bad_schema(self):
        val = JsonValidator()
        with self.assertRaises(jsonschema.exceptions.SchemaError):
            val.set_schema("asdf")

    def test_csv_validation(self):
        val = JsonValidator()
        val.set_local_schema("../test_schemas/car_schema.json")
        assert val.validate_csv("../test_data/car_sales.csv")
        with self.assertRaises(jsonschema.exceptions.ValidationError):
            val.validate_csv("../test_data/car_sales_bad.csv")
