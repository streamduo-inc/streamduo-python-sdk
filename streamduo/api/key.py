from nacl.encoding import Base64Encoder
from nacl.public import PrivateKey, PublicKey, SealedBox
from requests import Response

from streamduo.models.key_pair import KeyPair, KeyEncoding, KeyAlgorithm


class KeyController:
    """
    Provides methods for interacting with the `/key` endpoints
    """

    def __init__(self, client):
        self.client = client

    @staticmethod
    def create_key_local() -> tuple[KeyPair, str]:
        """
        Creates a new pub/priv keypair locally
        :return: (tuple) Public Key Object, Private Key String
        """
        ## create a secret Key
        sk = PrivateKey.generate()
        pk = KeyPair(publicKey=sk.public_key.encode(encoder=Base64Encoder).decode('utf8'),
                     publicKeyAlgorithm=KeyAlgorithm.CURVE25519.value,
                     publicKeyEncoding=KeyEncoding.BASE64.value)
        return  pk, sk.encode(encoder=Base64Encoder).decode('utf8')

    @staticmethod
    def get_public_key(key_string: str) -> PublicKey:
        """
        Converts a public Key String to a PublicKey Object
        :param key_string: Base64Encoded String of Public Key
        :return: PublicKey Object
        """
        return PublicKey(public_key=key_string.encode('utf-8'), encoder=Base64Encoder)

    @staticmethod
    def get_private_key(key_string: str) -> PrivateKey:
        """
        Converts a Private Key String to a PrivateKey Object
        :param key_string: Base64Encoded String of Private Key
        :return: PrivateKey Object
        """
        return PrivateKey(private_key=key_string.encode('utf-8'), encoder=Base64Encoder)

    @staticmethod
    def encrypt_file(key_string: str, source_file_path: str, destination_file_path: str):
        """
        Static Method for encrypting a file with a given public key String
        :param key_string: Base64Encoded String of public key
        :param source_file_path: filepath for source data
        :param destination_file_path: filepath for destination
        :return: None
        """
        sb = SealedBox(KeyController.get_public_key(key_string))
        with open(source_file_path, 'rb') as in_file:
            encrypted_data = sb.encrypt(in_file.read())
        with open(destination_file_path, 'wb') as out_file:
            out_file.write(encrypted_data)

    @staticmethod
    def decrypt_file(key_string: str, source_file_path: str, destination_file_path: str):
        """
         Static Method for decrypting a file with a given private key String
        :param key_string: Base64Encoded String of private key
        :param source_file_path:  filepath for source encrypted data
        :param destination_file_path:  filepath for destination decrypted data
        :return: None
        """
        unseal_box = SealedBox(KeyController.get_private_key(key_string))
        with open(source_file_path, 'rb') as in_file:
            out = unseal_box.decrypt(in_file.read())
        with open(destination_file_path, 'wb') as out_file:
            out_file.write(out)

    def upload_key(self, stream_id: str, key: str) -> Response:
        """
        Upload a locally generated public key to StreamDuo stream
        :param stream_id: ID of Stream to upload key to.
        :param key: Encoded string of public key.
        :return: requests.response object
        """
        return self.client.call_api('POST',
                                    f"/stream/{stream_id}/keys/",
                                    body=key.to_json())

    def set_active_key(self, stream_id: str, key_id: str) -> Response:
        """
        Set a key active on a streamDuo Stream
        :param stream_id: ID of Stream to set key active on
        :param key_id: ID of Key to set active
        :return: requests.response object
        """
        return self.client.call_api('POST',
                                    f"/stream/{stream_id}/keys/active",
                                    body={'keyId': key_id})

    def create_key_server(self, stream_id: str, key_request: dict) -> Response:
        """
        Server Side Key Creation
        :param stream_id: ID of Stream to create key on
        :param key_request: dict of request params
        :return:  requests.response object
        """
        return self.client.call_api('POST',
                                    f"/stream/{stream_id}/keys/generate",
                                    body=key_request)
