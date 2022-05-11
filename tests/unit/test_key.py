import filecmp
import os
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

    def test_encr_decr_file(self):
        original_file = "../test_data/car_sales.csv"
        encrypted_file = "../test_data/car_sales.csv.enc"
        decrypted_file = "../test_data/car_sales.csv.dec"
        pub, priv = KeyController.create_key_local()
        KeyController.encrypt_file(key_string=pub.publicKey, source_file_path=original_file,
                                   destination_file_path=encrypted_file)
        KeyController.decrypt_file(key_string=priv, source_file_path=encrypted_file,
                                   destination_file_path=decrypted_file)
        assert filecmp.cmp(original_file, decrypted_file) == True
        ## cleanup
        os.remove(encrypted_file)
        os.remove(decrypted_file)



