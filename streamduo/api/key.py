from nacl.encoding import Base64Encoder
from nacl.public import PrivateKey, PublicKey

from streamduo.models.key_pair import KeyPair, KeyEncoding, KeyAlgorithm


class KeyController:
    """
    Provides methods for interacting with the `/key` endpoints
    """

    def __init__(self, client):
        self.client = client

    @staticmethod
    def create_key_local():
        ## create a secret Key
        sk = PrivateKey.generate()
        pk = KeyPair(publicKey=sk.public_key.encode(encoder=Base64Encoder).decode('utf8'),
                     publicKeyAlgorithm=KeyAlgorithm.CURVE25519.value,
                     publicKeyEncoding=KeyEncoding.BASE64.value)
        return  pk, sk.encode(encoder=Base64Encoder).decode('utf8')

    @staticmethod
    def get_public_key(key_string: str) -> PublicKey:
        return PublicKey(public_key=key_string.encode('utf-8'), encoder=Base64Encoder)

    @staticmethod
    def get_private_key(key_string: str) -> PrivateKey:
        return PrivateKey(private_key=key_string.encode('utf-8'), encoder=Base64Encoder)

    def upload_key(self, stream_id, key):
        return self.client.call_api('POST',
                                    f"/stream/{stream_id}/keys/",
                                    body=key.to_json())

    def set_active_key(self, stream_id, key_id):
        return self.client.call_api('POST',
                                    f"/stream/{stream_id}/keys/active",
                                    body={'keyId': key_id})

    def create_key_server(self, stream_id, key_request):
        return self.client.call_api('POST',
                                    f"/stream/{stream_id}/keys/generate",
                                    body=key_request)