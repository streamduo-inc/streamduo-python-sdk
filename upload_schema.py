from streamduo.client import Client
import json

creds = {
        "streamId": "60c49e86-9db3-414a-87a1-f51ccee4ec0c",
        "clientId": "2v84gteih0ign6d32lca0flkrh",
        "clientSecret": "7pc74sgts0hnesupvklopmqefjvl2vd15k8chct7m4fpqfrt1oo"
      }

schema_controller = Client(creds['clientId'], creds['clientSecret']).get_schema_controller()
with open("tests/integration/car_schema.json", 'r') as file:
    car_schema = json.load(file)
create_schema_response1 = schema_controller.create_schema(stream_id=creds['streamId'], schema=car_schema, schema_type="JSON")
new_schema_id = create_schema_response1.json()['schemaId']
print(new_schema_id)
