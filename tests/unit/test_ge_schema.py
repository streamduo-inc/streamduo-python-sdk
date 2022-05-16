import os
from unittest import TestCase
from streamduo.validators.great_expectations_schema import GreatExepectationsValidator
import json
import great_expectations as ge

class TestGreatExpectations(TestCase):

    def test_csv_validation(self):
        my_expectation_suite = json.load(open("/Users/stevefrensch/dev/streamduo-python-sdk/tests/test_schemas/car_expectations.json"))
        my_df = ge.read_csv(
            f"{os.getcwd()}/unit_test_data/car_sales.csv",
            expectation_suite=my_expectation_suite
        )
        validation_results = my_df.validate()
        assert validation_results['success']

        val = GreatExepectationsValidator()
        val.set_expectations("/Users/stevefrensch/dev/streamduo-python-sdk/tests/test_schemas/car_expectations.json")
        val.validate_csv(f"{os.getcwd()}/unit_test_data/car_sales.csv")
