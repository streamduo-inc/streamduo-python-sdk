import os
from unittest import TestCase
from streamduo.validators.frictionless_schema import validate_schema, FrictionValidator
from frictionless import describe
import pprint as pp


class TestFriction(TestCase):

    def test_csv_validation(self):
        val = FrictionValidator()
        val.set_schema("../test_schemas/car_schema.friction")
        val.validate_csv("unit_test_data/car_sales.csv")

