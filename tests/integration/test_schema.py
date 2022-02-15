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

        ## Check if in schema is in user object
        actor_controller = Client(os.getenv('AUTH_CLIENT_ID'), os.getenv('AUTH_CLIENT_SECRET')).get_actor_controller()
        user_response = actor_controller.get_user()
        found = False
        for p in user_response.json()['schemaPermissionList']:
            if p['schemaId'] == new_schema_id:
                found = True
                break
        assert found == True

        ## BAD Schema errors out
        car_schema['properties']['Make']['$id'] = "#root/Make 2"
        create_schema_response2 = schema_controller.create_schema(car_schema, "JSON")
        assert create_schema_response2.status_code == 400

        ## cleanup
        delete_response = schema_controller.delete_schema(schema_id=new_schema_id, schema_version="1")
        assert delete_response.status_code == 200

        ## Check if schema is in user object
        user_response_2 = actor_controller.get_user()
        found = False
        for p in user_response_2.json()['schemaPermissionList']:
            if p['schemaId'] == new_schema_id:
                found = True
                break
        assert found == False
