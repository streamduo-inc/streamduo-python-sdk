import requests
from streamduo.api.health import Health
from streamduo.api.stream import Stream
from streamduo.api.actor import Actor
from streamduo.api.record import Record

class Client:
    def __init__(self, client_id, client_secret):
        """Constructor"""
        self.auth_endpoint = "https://dev-v475zrua.us.auth0.com/oauth/token"
        self.api_endpoint = "https://api.streamduo.com"
        self.client_id = client_id
        self.client_secret = client_secret
        self.token = None
        self.set_oauth_token()

    def set_oauth_token(self):
        header = {'content-type': 'application/x-www-form-urlencoded'}
        token_req_payload = {'grant_type': 'client_credentials',
                             'client_id': self.client_id,
                             'client_secret': self.client_secret,
                             'audience': 'https://api.streamduo.com'}
        token_response = requests.post(self.auth_endpoint,
                                       data=token_req_payload,
                                       headers=header)
        self.token = token_response.json()['access_token']

    def call_api(self, verb, path, body=None):
        header = {'authorization': f"Bearer {self.token}",
                'content-type': 'application/json'}
        if verb == 'GET':
            return requests.get(f"{self.api_endpoint}{path}",
                                headers=header)
        if verb == 'POST':
            return requests.post(f"{self.api_endpoint}{path}",
                                headers=header,
                                json=body)
        if verb == 'DELETE':
            return requests.delete(f"{self.api_endpoint}{path}",
                                headers=header,
                                json=body)

    def get_health_controller(self):
        return Health(self)

    def get_stream_controller(self):
        return Stream(self)

    def get_actor_controller(self):
        return Actor(self)

    def get_record_controller(self):
        return Record(self)
