import json
import pprint
from unittest import TestCase
from streamduo.api.batch import BatchController

import os

class TestJson(TestCase):

    def test_construct_init(self):
        FILE_SIZE = 1024 * 1024 * 100  # 100 mb
        BUF_SIZE = 1024 * 1024 *5  # 5 MB
        big_file = "unit_test_data/bigfile.dat"
        # multiply file
        with open(big_file, 'wb') as out_file:
            out_file.write(os.urandom(FILE_SIZE))

        req = BatchController.construct_batch_init_request(big_file, BUF_SIZE)
        pprint.pprint(req.to_json())
        # cleanup
        os.remove(big_file)

    def test_get_part_binary(self):
        FILE_SIZE = 1024 * 1024 * 100  # 100 mb
        BUF_SIZE = 1024 * 1024 *5  # 5 MB
        big_file = "unit_test_data/bigfile.dat"
        # multiply file
        with open(big_file, 'wb') as out_file:
            out_file.write(os.urandom(FILE_SIZE))
        bin_part = BatchController.get_part_binary(file_path=big_file, part_number=4, BUF_SIZE=BUF_SIZE)

        req = BatchController.construct_batch_init_request(big_file, BUF_SIZE)
        print(req.partList)



