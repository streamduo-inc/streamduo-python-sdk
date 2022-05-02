import base64
import hashlib
import json
import pprint
from unittest import TestCase
from streamduo.api.batch import BatchController

import os

class TestJson(TestCase):

    def test_construct_init(self):
        FILE_SIZE = 1024 * 1024 * 100  # 100 mb
        big_file = "unit_test_data/bigfile.dat"
        # multiply file
        with open(big_file, 'wb') as out_file:
            out_file.write(os.urandom(FILE_SIZE))

        req = BatchController.construct_batch_init_request(big_file)
        pprint.pprint(req.to_json())
        assert len(req.hashes.keys()) == 20
        # cleanup
        os.remove(big_file)

    def test_get_part_binary(self):
        FILE_SIZE = 1024 * 1024 * 100  # 100 mb
        big_file = "unit_test_data/bigfile.dat"
        PART_NUMBER = '4'
        # multiply file
        with open(big_file, 'wb') as out_file:
            out_file.write(os.urandom(FILE_SIZE))
        bin_part = BatchController.get_part_binary(file_path=big_file, part_number=PART_NUMBER)

        req = BatchController.construct_batch_init_request(big_file)

        assert req.hashes[int(PART_NUMBER)] == base64.b64encode(hashlib.md5(bin_part).digest()).decode()



