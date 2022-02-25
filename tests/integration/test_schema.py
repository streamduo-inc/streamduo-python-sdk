import os
import json
from unittest import TestCase

import jsonschema

from streamduo.client import Client
from streamduo.validators.json_schema import JsonValidator
from streamduo.models.schema import SchemaType

class TestStream(TestCase):

    def test_create_schema(self):

        ##create a stream
        display_name = 'test_stream'
        stream_controller = Client(os.getenv('AUTH_CLIENT_ID'), os.getenv('AUTH_CLIENT_SECRET')).get_stream_controller()
        stream_request_result = stream_controller.create_stream(display_name)
        stream_id = stream_request_result.json()['streamId']
        assert stream_request_result.json()['displayName'] == display_name

        ## Add schema to stream
        schema_controller = Client(os.getenv('AUTH_CLIENT_ID'), os.getenv('AUTH_CLIENT_SECRET')).get_schema_controller()
        with open("car_schema.json", 'r') as file:
            car_schema = json.load(file)
        create_schema_response1 = schema_controller.create_schema(stream_id=stream_id,
                                                                  schema=car_schema, schema_type=SchemaType.JSON)
        new_schema_id = create_schema_response1.json()['schemaId']
        assert new_schema_id is not None

        ## BAD Schema errors out
        car_schema['properties']['Make']['$id'] = "#root/Make 2"
        create_schema_response2 = schema_controller.create_schema(stream_id=stream_id,
                                                                  schema=car_schema, schema_type=SchemaType.JSON)
        assert create_schema_response2.status_code == 400

        ## cleanup schema
        delete_response = schema_controller.delete_schema(schema_id=new_schema_id, stream_id=stream_id)
        assert delete_response.status_code == 204

        ## Cleanup stream
        delete_response_stream = stream_controller.delete_stream(stream_request_result.json()['streamId'])
        assert delete_response_stream.status_code == 204

    def test_read_schema(self):

        ##create a stream
        display_name = 'test_stream'
        stream_controller = Client(os.getenv('AUTH_CLIENT_ID'), os.getenv('AUTH_CLIENT_SECRET')).get_stream_controller()
        stream_request_result = stream_controller.create_stream(display_name)
        stream_id = stream_request_result.json()['streamId']
        assert stream_request_result.json()['displayName'] == display_name

        ## Add schema to stream
        schema_controller = Client(os.getenv('AUTH_CLIENT_ID'), os.getenv('AUTH_CLIENT_SECRET')).get_schema_controller()
        with open("car_schema.json", 'r') as file:
            car_schema = json.load(file)
        create_schema_response1 = schema_controller.create_schema(stream_id=stream_id,
                                                                  schema=car_schema, schema_type=SchemaType.JSON)
        new_schema_id = create_schema_response1.json()['schemaId']
        assert new_schema_id is not None

        ## get schema
        schema_response = schema_controller.get_schema(stream_id=stream_id, schema_id=new_schema_id)
        schema = schema_response.get_schema()
        assert schema['$id'] == 'https://example.com/object1644429127.json'

        ## test an object w schema
        val = JsonValidator()
        val.set_schema(schema=schema)
        valid_rec = {
            "Make": "Nissan",
            "Price": "$9,700.00",
            "Odometer (KM)": "31600",
            "Colour": "White",
            "Doors": "4"
        }
        assert val.validate_record(valid_rec)

        bad_rec = {
            "Make": "Nissan",
            "Price": "$9,700.00",
            "Odometer (KM)": "31600",
            "Colour": "White"
        }
        with self.assertRaises(jsonschema.exceptions.ValidationError):
            val.validate_record(bad_rec)

        ## cleanup schema
        delete_response = schema_controller.delete_schema(schema_id=new_schema_id, stream_id=stream_id)
        assert delete_response.status_code == 204

        ## Cleanup stream
        delete_response_stream = stream_controller.delete_stream(stream_request_result.json()['streamId'])
        assert delete_response_stream.status_code == 204