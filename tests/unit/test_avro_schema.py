from unittest import TestCase

import fastavro

from streamduo.validators.avro_schema import AvroValidator


class TestJson(TestCase):

    def test_json_record_validation(self):
        val = AvroValidator()
        val.set_local_schema("../test_schemas/car_schema.avsc")
        valid_rec = {
            "Make": "Nissan",
            "Price": "$9,700.00",
            "Odometer (KM)": "31600",
            "Colour": "White",
            "Doors": "4"
        }
        assert val.validate_record(valid_rec)
        inval_rec = valid_rec.copy()
        inval_rec['Odometer (KM)'] = "xyz"
        with self.assertRaises(fastavro._validate_common.ValidationError):
            val.validate_record(inval_rec)