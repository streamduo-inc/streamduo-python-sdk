import os
import requests

class AuthManager:
    def __init__(self):
        self.AUTH_CLIENT_ID = os.getenv("AUTH_CLIENT_ID")
        self.AUTH_CLIENT_SECRET = os.getenv("AUTH_CLIENT_SECRET")
        self.AUTH_URL = os.getenv("AUTH_URL")
        self.ENDPOINT_BASE_URL = "http://localhost:8081"
        self.header = self.get_header()

    def get_oauth_token(self):
        print(self.AUTH_URL)
        header = {'content-type': 'application/x-www-form-urlencoded'}
        token_req_payload = {'grant_type': 'client_credentials',
                             'client_id': self.AUTH_CLIENT_ID,
                             'client_secret': self.AUTH_CLIENT_SECRET,
                             'audience': 'https://api.streamduo.com'}
        token_response = requests.post(self.AUTH_URL,
            data=token_req_payload, headers=header)
        return token_response.json()

    def get_header(self):
        return {'authorization': f"Bearer {self.get_oauth_token()['access_token']}",
                'content-type': 'application/json'}

    def get_health(self):
        health = requests.get(f"{self.ENDPOINT_BASE_URL}/health")
        return(health.text)

    def get_table_list(self):
        table_response = requests.get(f"{self.ENDPOINT_BASE_URL}/stream/list", headers=self.header)
        return table_response.json()['tableNames']