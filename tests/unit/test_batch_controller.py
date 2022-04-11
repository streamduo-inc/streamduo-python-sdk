import json
import uuid
from unittest import TestCase
from streamduo.api.batch import BatchController

import os
import hashlib

class TestJson(TestCase):

    def test_construct_init(self):
        FILE_SIZE = 1024 * 1024 * 1024  # 1GB
        BUF_SIZE = 1024 * 1024 *5  # 5 MB
        big_file = "unit_test_data/bigfile.dat"
        # multiply file
        with open(big_file, 'wb') as out_file:
            out_file.write(os.urandom(FILE_SIZE))

        req = BatchController.construct_batch_init_request(big_file, BUF_SIZE)
        print(json.dumps(req, default=lambda x: x.__dict__))
        # cleanup
        os.remove(big_file)


