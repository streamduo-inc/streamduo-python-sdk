import pprint
from unittest import TestCase

from nacl.encoding import Base64Encoder
from nacl.public import PublicKey, SealedBox, PrivateKey

from streamduo.api.key import KeyController


class TestKey(TestCase):

    def test_create_key(self):
        pub, priv = KeyController.create_key()
        assert len(priv) == 44

    def test_encr_decr(self):
        pub, priv = KeyController.create_key()
        ## Get pub Key Bytes
        consumer_pk = PublicKey(public_key=pub.publicKey, encoder=Base64Encoder)
        sb = SealedBox(consumer_pk)
        with open("../test_data/car_sales.csv", 'rb') as file:
            enc = sb.encrypt(file.read())
            print(sb)
            unseal_box = SealedBox(PrivateKey(private_key=priv.encode('utf-8'), encoder=Base64Encoder))
            out = unseal_box.decrypt(enc)
            print(out.decode('utf-8'))



