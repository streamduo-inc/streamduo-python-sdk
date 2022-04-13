import os
from unittest import TestCase

from streamduo.client import Client
from streamduo.models.batch_data import BatchData


class TestActor(TestCase):

    def test_create_machine_client(self):
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
        print(resp.json())
        batch_data = BatchData(**resp.json())
        print(batch_data)

        ## Cleanup
        stream_controller.delete_stream(new_stream_id)