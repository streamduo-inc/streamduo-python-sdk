
from unittest import TestCase

from nacl.public import SealedBox

from streamduo.api.key import KeyController


class TestKey(TestCase):

    def test_create_key(self):
        pub, priv = KeyController.create_key_local()
        assert len(priv) == 44

    def test_encr_decr(self):
        ##Key Object, priv key (string)
        pub, priv = KeyController.create_key_local()
        sb = SealedBox(KeyController.get_public_key(pub.publicKey))
        with open("../test_data/car_sales.csv", 'rb') as file:
            encrypted_data = sb.encrypt(file.read())
        unseal_box = SealedBox(KeyController.get_private_key(priv))
        out = unseal_box.decrypt(encrypted_data)
        print(out.decode('utf-8'))



