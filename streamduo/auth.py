import os
import requests

AUTH_CLIENT_ID = os.getenv("AUTH_CLIENT_ID")
AUTH_CLIENT_SECRET = os.getenv("AUTH_CLIENT_SECRET")
AUTH_URL =  os.getenv("AUTH_URL")
ENDPOINT_BASE_URL = "http://localhost:8080"

def get_oauth_token():
    print(AUTH_URL)
    header = {'content-type': 'application/x-www-form-urlencoded'}
    token_req_payload = {'grant_type': 'client_credentials',
                         'client_id': AUTH_CLIENT_ID,
                         'client_secret': AUTH_CLIENT_SECRET,
                         'audience': 'https://api.streamduo.com'}
    token_response = requests.post(AUTH_URL,
        data=token_req_payload, headers=header)
    return token_response.json()

def get_header():
    return {'authorization': f"Bearer {get_oauth_token()['access_token']}",
            'content-type': 'application/json'}

def get_health():
    health = requests.get(f"{ENDPOINT_BASE_URL}/health")
    print(health)