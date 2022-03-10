from streamduo.client import Client
import json

creds = {
        "streamId": "a440ada0-7e25-473d-8c19-da0f51c5ae56",
        "clientId": "6a9ser1q6up3i12001q9ap7q9g",
        "clientSecret": "1ogk9db7mf3o0u75qp5km7it8emopn9rk9tbr4qrrbc1rul2u698"
      }

schema_controller = Client(creds['clientId'], creds['clientSecret']).get_schema_controller()
with open("tests/test_schemas/car_expectations.json", 'r') as file:
    car_schema = json.load(file)
create_schema_response1 = schema_controller.create_schema(stream_id=creds['streamId'], schema=car_schema, schema_type="GREAT_EXPECTATIONS")
new_schema_id = create_schema_response1.json()['schemaId']
print(new_schema_id)
