from streamduo.client import Client
import json
import requests

creds = {
        "streamId": "a440ada0-7e25-473d-8c19-da0f51c5ae56",
        "clientId": "6a9ser1q6up3i12001q9ap7q9g",
        "clientSecret": "1ogk9db7mf3o0u75qp5km7it8emopn9rk9tbr4qrrbc1rul2u698"
      }

record_controller = Client(creds['clientId'], creds['clientSecret']).get_record_controller()

req_header = {'authorization': f"Bearer {record_controller.client.token}"}

with open("tests/test_data/car_sales.csv", 'r') as file:
    files = {'file': file}
    resp = requests.post(f"{record_controller.client.api_endpoint}/stream/{creds['streamId']}/file",
                                 headers=req_header,
                                 files=files)

print(resp)