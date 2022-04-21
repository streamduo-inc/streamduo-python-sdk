import os
import pprint
from unittest import TestCase

from streamduo.client import Client
from streamduo.models.batch_data import BatchData
from streamduo.api.batch import BatchController


class TestBatch(TestCase):

    def test_init_batch(self):
        display_name = 'batch_test_stream'
        stream_controller = Client(os.getenv('AUTH_CLIENT_ID'), os.getenv('AUTH_CLIENT_SECRET')).get_stream_controller()
        new_stream_id = stream_controller.create_stream(display_name).json()['streamId']

        batch_controller = Client(os.getenv('AUTH_CLIENT_ID'), os.getenv('AUTH_CLIENT_SECRET')).get_batch_controller()
        FILE_SIZE = 1024 * 1024 * 100  # 1GB
        BUF_SIZE = 1024 * 1024 *5  # 5 MB
        big_file = "bigfile.dat"
        # multiply file
        with open(big_file, 'wb') as out_file:
            out_file.write(os.urandom(FILE_SIZE))

        resp = batch_controller.send_batch_init(stream_id=new_stream_id, file_path=big_file, BUF_SIZE=BUF_SIZE)
        batch_data = BatchData(**resp.json())
        assert len(batch_data.outstandingParts.keys()) == 20
        ## Cleanup
        stream_controller.delete_stream(new_stream_id)

    def test_send_part(self):
        display_name = 'batch_test_stream'
        stream_controller = Client(os.getenv('AUTH_CLIENT_ID'), os.getenv('AUTH_CLIENT_SECRET')).get_stream_controller()
        new_stream_id = stream_controller.create_stream(display_name).json()['streamId']

        batch_controller = Client(os.getenv('AUTH_CLIENT_ID'), os.getenv('AUTH_CLIENT_SECRET')).get_batch_controller()
        FILE_SIZE = 1024 * 1024 * 100  # 1GB
        BUF_SIZE = 1024 * 1024 *5  # 5 MB
        big_file = "bigfile.dat"
        # multiply file
        with open(big_file, 'wb') as out_file:
            out_file.write(os.urandom(FILE_SIZE))

        resp = batch_controller.send_batch_init(stream_id=new_stream_id, file_path=big_file, BUF_SIZE=BUF_SIZE)
        batch_data = BatchData(**resp.json())
        part_bin = BatchController.get_part_binary(file_path=big_file, part_number=5, BUF_SIZE=BUF_SIZE)
        ## Send part 5
        batch_data_resp = batch_controller.send_batch_part(batch_data=batch_data, part_number=5, binary_payload=part_bin)
        batch_data_2 = BatchData(**batch_data_resp.json())
        pprint.pprint(batch_data_2.to_json())
        assert '5' not in batch_data_2.outstandingParts.keys()
        ## Cleanup
        stream_controller.delete_stream(new_stream_id)