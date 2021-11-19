import os

import requests
from streamduo.api.health import HealthController
from streamduo.api.stream import StreamController
from streamduo.api.actor import ActorController
from streamduo.api.record import RecordController

class Client:
    """
    The Client Object manages authorization headers for API calls.
    controllers are generated from this Client Object, and are provided
    with the authorization support for their methods.
    """
    def __init__(self, client_id, client_secret):
        """
        Constructor for Client object.
        :param client_id: StreamDuo Client ID
        :param client_secret: StreamDuo Client Secret
        """
        self.auth_endpoint = "https://streamduo.us.auth0.com/oauth/token"
        if os.getenv('STREAMDUO_SDK_URL'):
            self.api_endpoint = os.getenv('STREAMDUO_SDK_URL')
        else:
            self.api_endpoint = "https://api.streamduo.com"

        self.client_id = client_id
        self.client_secret = client_secret
        self.token = None
        self.auth_req_header = {'content-type': 'application/x-www-form-urlencoded'}
        self.token_req_payload = {'grant_type': 'client_credentials',
                                  'client_id': self.client_id,
                                  'client_secret': self.client_secret,
                                  'audience': 'https://api.streamduo.com'}
        self.set_oauth_token()

    def set_oauth_token(self):
        """
        Method to set the OAUTH token
        :return: None
        """
        try:
            token_response = requests.post(self.auth_endpoint,
                                           data=self.token_req_payload,
                                           headers=self.auth_req_header)
            self.token = token_response.json()['access_token']
        except KeyError:
            self.token = None

    def call_api(self, verb, path, body=None, files=None):
        """
        Generic function to call the SteamDuo APIs.
        Authorization and headers are managed prior to calling API.
        :param verb: HTTP Verb (GET, POST, DELETE)
        :param path: URL path excluding base URL (i.e. /stream)
        :param body: Body of request if one is used. This can be either a dict, or a JSON formatted String.
        :param files: A File Object of any file used in the API call.
        :return: Requests Response Object of the API call.
        """
        header = {'authorization': f"Bearer {self.token}",
                  'content-type': 'application/json'}
        if verb == 'GET':
            return requests.get(f"{self.api_endpoint}{path}",
                                headers=header)
        if verb == 'POST':
            if files:
                del header['content-type']
            return requests.post(f"{self.api_endpoint}{path}",
                                 headers=header,
                                 files=files,
                                 json=body)
        if verb == 'DELETE':
            return requests.delete(f"{self.api_endpoint}{path}",
                                   headers=header,
                                   json=body)
        return None

    def get_health_controller(self):
        """
        Provides a health controller to access /health endpoints
        :return: HealthController
        """
        return HealthController(self)

    def get_stream_controller(self):
        """
        Provides a Stream controller to access /stream endpoints
        :return: StreamController
        :return:
        """
        return StreamController(self)


    def get_actor_controller(self):
        """
        Provides an Actor controller to access /client endpoints.
        :return: ActorController
        """
        return ActorController(self)

    def get_record_controller(self):
        """
        Provides a Record Controller to interact with reading/writing streams
        :return: RecordController
        """
        return RecordController(self)
