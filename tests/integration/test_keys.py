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
        key_controller.upload_key(stream_id=new_stream_id, key=pub_key)

        assert True

    def test_create_key(self):
        assert True
