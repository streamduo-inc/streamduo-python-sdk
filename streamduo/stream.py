from auth import *
import requests
import json



def get_oauth_token():
    token_req_payload = {'grant_type': 'client_credentials'}
    token_response = requests.post(AUTH_URL,
        data=token_req_payload, verify=False, allow_redirects=False,
        auth=(AUTH_CLIENT_ID, AUTH_CLIENT_SECRET))
    return token_response.json()



