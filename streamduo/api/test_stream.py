from unittest import TestCase
import os
from streamduo.client import Client


class TestStream(TestCase):


    def test_create_stream(self):
        display_name = 'test_stream'
        stream_controller = Client(os.getenv('AUTH_CLIENT_ID'), os.getenv('AUTH_CLIENT_SECRET')).get_stream_controller()
        stream_request_result = stream_controller.create_stream(display_name)
        assert stream_request_result.json()['displayName'] == display_name
        ## Cleanup
        stream_controller.delete_stream(stream_request_result.json()['streamId'])

    def test_get_stream(self):
        display_name = 'test_stream'
        stream_controller = Client(os.getenv('AUTH_CLIENT_ID'), os.getenv('AUTH_CLIENT_SECRET')).get_stream_controller()
        new_stream_id = stream_controller.create_stream(display_name).json()['streamId']
        stream_request_result = stream_controller.get_stream(new_stream_id)
        assert stream_request_result.json()['streamId'] == new_stream_id
        ## Cleanup
        stream_controller.delete_stream(new_stream_id)

    def test_delete_stream(self):
        display_name = 'test_stream'
        stream_controller = Client(os.getenv('AUTH_CLIENT_ID'), os.getenv('AUTH_CLIENT_SECRET')).get_stream_controller()
        new_stream_id = stream_controller.create_stream(display_name).json()['streamId']
        stream_request_result = stream_controller.get_stream(new_stream_id)
        ## Assert was created
        assert stream_request_result.json()['streamId'] == new_stream_id
        stream_delete_result = stream_controller.delete_stream(new_stream_id)
        assert stream_delete_result.status_code == 204
        ## Assert 404
        stream_request_result_2 = stream_controller.get_stream(new_stream_id)
        assert stream_request_result_2.status_code == 404

