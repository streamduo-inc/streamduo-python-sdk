from nacl.encoding import Base64Encoder
from nacl.public import PrivateKey

from streamduo.models.key_pair import KeyPair, KeyEncoding, KeyAlgorithm


class KeyController:
    """
    Provides methods for interacting with the `/key` endpoints
    """

    def __init__(self, client):
        self.client = client

    @staticmethod
    def create_key():
        ## create a secret Key
        sk = PrivateKey.generate()
        pk = KeyPair(publicKey=sk.public_key.encode(encoder=Base64Encoder).decode('utf8'),
                     publicKeyAlgorithm=KeyAlgorithm.CURVE25519.value,
                     publicKeyEncoding=KeyEncoding.BASE64.value)
        return  pk, sk.encode(encoder=Base64Encoder).decode('utf8')

    def upload_key(self, stream_id, key):
        return self.client.call_api('POST',
                                    f"/stream/{stream_id}/keys/",
                                    body=key.to_json())
