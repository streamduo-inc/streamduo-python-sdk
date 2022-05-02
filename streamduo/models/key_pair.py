
from enum import Enum


class KeyAlgorithm(Enum):
    CURVE25519 = 'CURVE25519'

class KeyEncoding(Enum):
    BASE64 = 'BASE64'


class KeyPair:
    """
    Class for keypairs
    """
    def __init__(self, publicKeyId=None, publicKeyAlgorithm=None, publicKeyVersion=None, publicKeyEncoding=None, publicKey=None, publicKeyDescription=None ):
        """
         Constructor
         """
        self.publicKeyId = publicKeyId
        self.publicKeyAlgorithm = publicKeyAlgorithm
        self.publicKeyVersion = publicKeyVersion
        self.publicKeyEncoding = publicKeyEncoding
        self.publicKey = publicKey
        self.publicKeyDescription = publicKeyDescription

    def to_json(self):
        return self.__dict__