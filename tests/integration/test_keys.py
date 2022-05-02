import os
from unittest import TestCase

from streamduo.api.key import KeyController
from streamduo.client import Client


class TestKeys(TestCase):

    def setUp(self) -> None:
        self.api_client = Client(os.getenv('AUTH_CLIENT_ID'), os.getenv('AUTH_CLIENT_SECRET'))

    def test_write_key(self):
        display_name = 'batch_test_key'
        stream_controller = self.api_client.get_stream_controller()
        new_stream_id = stream_controller.create_stream(display_name).json()['streamId']

        pub_key, priv_key = KeyController.create_key()
        key_controller = self.api_client.get_key_controller()
        upload_response = key_controller.upload_key(stream_id=new_stream_id, key=pub_key)
        key_id = upload_response.json()['publicKeyId']
        assert key_id is not None

        ## Set Active
        active_response = key_controller.set_active_key(stream_id=new_stream_id, key_id=key_id)
        assert active_response.status_code == 200
        assert self.api_client.get_stream_controller().get_stream(new_stream_id).json()['activeKeyId'] == key_id


    def test_create_key(self):
        assert True
