import os
import json
from unittest import TestCase
from streamduo.client import Client

class TestStream(TestCase):

    def test_create_schema(self):

        schema_controller = Client(os.getenv('AUTH_CLIENT_ID'), os.getenv('AUTH_CLIENT_SECRET')).get_schema_controller()
        with open("car_schema.json", 'r') as file:
            car_schema = json.load(file)
        create_schema_response1 = schema_controller.create_schema(car_schema, "JSON")
        new_schema_id = create_schema_response1.json()['schemaId']
        assert new_schema_id is not None

        assert schema_controller.delete_schema(new_schema_id, "1").status_code == 200

        car_schema['properties']['Make']['$id'] = "#root/Make 2"
        create_schema_response2 = schema_controller.create_schema(car_schema, "JSON")
        assert create_schema_response2.status_code == 400

        # ## cleanup
        # delete_response = actor_controller.delete_machine_client(new_client_id)
        # assert delete_response.status_code == 200
        #
        # ## check get
        # get_response = actor_controller.get_machine_client(new_client_id)
        # assert get_response.status_code == 404