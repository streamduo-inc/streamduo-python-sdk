import os
import pprint
from unittest import TestCase

from nacl.public import SealedBox

from streamduo.api.key import KeyController
from streamduo.client import Client
from streamduo.models.key_pair import KeyAlgorithm, KeyEncoding


class TestKeys(TestCase):

    def setUp(self) -> None:
        self.api_client = Client(os.getenv('AUTH_CLIENT_ID'), os.getenv('AUTH_CLIENT_SECRET'))

    def test_write_key(self):
        display_name = 'test_write_key'
        stream_controller = self.api_client.get_stream_controller()
        new_stream_id = stream_controller.create_stream(display_name).json()['streamId']

        pub_key, priv_key = KeyController.create_key_local()
        key_controller = self.api_client.get_key_controller()
        upload_response = key_controller.upload_key(stream_id=new_stream_id, key=pub_key)
        key_id = upload_response.json()['publicKeyId']
        assert key_id is not None

        ## Set Active
        active_response = key_controller.set_active_key(stream_id=new_stream_id, key_id=key_id)
        assert active_response.status_code == 200
        assert self.api_client.get_stream_controller().get_stream(new_stream_id).json()['activeKeyId'] == key_id

    def test_generate_key(self):
        display_name = 'test_generate_key'
        stream_controller = self.api_client.get_stream_controller()
        new_stream_id = stream_controller.create_stream(display_name).json()['streamId']
        key_controller = self.api_client.get_key_controller()
        key_request = {'publicKeyAlgorithm': KeyAlgorithm.CURVE25519.value,
                       'publicKeyEncoding': KeyEncoding.BASE64.value,
                       'publicKeyDescription': "test key integraiton"}
        new_key_resp = key_controller.create_key_server(new_stream_id, key_request)
        pprint.pprint(new_key_resp.json())
        priv = new_key_resp.json()['privateKeyValue']
        pub = new_key_resp.json()['publicKey']['publicKeyValue']

        sb = SealedBox(KeyController.get_public_key(pub))
        unencrypted_data = b'super secret bytes'
        encrypted_data = sb.encrypt(unencrypted_data)
        unseal_box = SealedBox(KeyController.get_private_key(priv))
        assert unseal_box.decrypt(encrypted_data) == unencrypted_data
