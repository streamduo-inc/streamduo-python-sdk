import os

import requests

from streamduo.api.batch import BatchController
from streamduo.api.health import HealthController
from streamduo.api.key import KeyController
from streamduo.api.stream import StreamController
from streamduo.api.actor import ActorController
from streamduo.api.record import RecordController
from streamduo.api.schema import SchemaController


class Client:
    """
    The Client Object manages authorization headers for API calls.
    controllers are generated from this Client Object, and are provided
    with the authorization support for their methods.
    """
    auth_endpoint = "https://streamduo-authentication.auth.us-east-1.amazoncognito.com/oauth2/token"
    api_endpoint = "https://api.streamduo.com"
    stream_scope = "https://api.streamduo.com/manage:streams"
    record_scope = "https://api.streamduo.com/read:records"

    def __init__(self, client_id, client_secret):
        """
        Constructor for Client object.
        :param client_id: StreamDuo Client ID
        :param client_secret: StreamDuo Client Secret
        """
        self.auth_endpoint = Client.auth_endpoint
        self.scope = ''
        if os.getenv('STREAMDUO_SDK_URL'):
            self.api_endpoint = os.getenv('STREAMDUO_SDK_URL')
        else:
            self.api_endpoint = Client.api_endpoint

        self.client_id = client_id
        self.client_secret = client_secret
        self.token = None
        self.auth_req_header = {'content-type': 'application/x-www-form-urlencoded'}
        self.token_req_payload = {'grant_type': 'client_credentials',
                                  'client_id': self.client_id,
                                  'client_secret': self.client_secret}

    def set_oauth_token(self, scope):
        """
        Method to set the OAUTH token
        :return: None
        """
        self.scope = scope
        self.token_req_payload['scope'] = self.scope
        try:
            token_response = requests.post(self.auth_endpoint,
                                           data=self.token_req_payload,
                                           headers=self.auth_req_header)
            token_response.raise_for_status()
            self.token = token_response.json()['access_token']

        except KeyError:
            self.token = None

    def call_api(self, verb, path, params=None, body=None, files=None):
        """
        Generic function to call the SteamDuo APIs.
        Authorization and headers are managed prior to calling API.
        :param verb: HTTP Verb (GET, POST, DELETE)
        :param path: URL path excluding base URL (i.e. /stream)
        :param params: dict of querystring params
        :param body: Body of request if one is used. This can be either a dict, or a JSON formatted String.
        :param files: A File Object of any file used in the API call.
        :return: Requests Response Object of the API call.
        """
        header = {'authorization': f"Bearer {self.token}",
                  'content-type': 'application/json'}
        if verb == 'GET':
            response = requests.get(f"{self.api_endpoint}{path}",
                                    params=params,
                                    headers=header)
        if verb == 'POST':
            if files:
                del header['content-type']
            response = requests.post(f"{self.api_endpoint}{path}",
                                     headers=header,
                                     files=files,
                                     json=body)
        if verb == 'DELETE':
            response = requests.delete(f"{self.api_endpoint}{path}",
                                       headers=header,
                                       json=body)
        response.raise_for_status()
        return response

    def get_health_controller(self):
        """
        Provides a health controller to access /health endpoints
        :return: HealthController
        """
        if self.scope != Client.stream_scope or self.token is None:
            self.set_oauth_token(Client.stream_scope)
        return HealthController(self)

    def get_stream_controller(self):
        """
        Provides a Stream controller to access /stream endpoints
        :return: StreamController
        :return:
        """
        if self.scope != Client.stream_scope or self.token is None:
            self.set_oauth_token(Client.stream_scope)
        return StreamController(self)

    def get_actor_controller(self):
        """
        Provides an Actor controller to access /client endpoints.
        :return: ActorController
        """
        if self.scope != Client.stream_scope or self.token is None:
            self.set_oauth_token(Client.stream_scope)
        return ActorController(self)

    def get_record_controller(self):
        """
        Provides a Record Controller to interact with reading/writing streams
        :return: RecordController
        """
        if self.scope != Client.record_scope or self.token is None:
            self.set_oauth_token(Client.record_scope)
        return RecordController(self)

    def get_schema_controller(self):
        """
        Provides a Schema Controller to interact with schema endpoints
        :return: SchemaController
        """
        if self.scope != Client.stream_scope or self.token is None:
            self.set_oauth_token(Client.record_scope)
        return SchemaController(self)

    def get_batch_controller(self):
        if self.scope != Client.record_scope or self.token is None:
            self.set_oauth_token(Client.record_scope)
        return BatchController(self)

    def get_key_controller(self):
        """
        Provides a Record Controller to interact with reading/writing streams
        :return: RecordController
        """
        if self.scope != Client.record_scope or self.token is None:
            self.set_oauth_token(Client.record_scope)
        return KeyController(self)