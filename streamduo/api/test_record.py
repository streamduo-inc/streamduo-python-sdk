from unittest import TestCase
import os
from streamduo.client import Client

class TestRecord(TestCase):
    def test_write_record(self):
        display_name = 'test_stream'
        stream_controller = Client(os.getenv('AUTH_CLIENT_ID'), os.getenv('AUTH_CLIENT_SECRET')).get_stream_controller()
        stream_request_result = stream_controller.create_stream(display_name)
        stream_id = stream_request_result.json()['streamId']

        record_controller = Client(os.getenv('AUTH_CLIENT_ID'), os.getenv('AUTH_CLIENT_SECRET')).get_record_controller()
        payload = {'level_1a': [{'level_2a': 99},
                               {'level_2b': 'wayne'}],
                   'level_1b': 'some text'
                   }
        write_response = record_controller.write_record(stream_id, payload)
        assert write_response.json()['dataPayload']['level_1b'] == 'some text'

        ## Cleanup
        stream_controller.delete_stream(stream_id)

    def test_read_simple_record(self):
        display_name = 'test_stream'
        stream_controller = Client(os.getenv('AUTH_CLIENT_ID'),
                                   os.getenv('AUTH_CLIENT_SECRET')).get_stream_controller()
        stream_request_result = stream_controller.create_stream(display_name)
        stream_id = stream_request_result.json()['streamId']

        record_controller = Client(os.getenv('AUTH_CLIENT_ID'),
                                   os.getenv('AUTH_CLIENT_SECRET')).get_record_controller()
        payload = {'level_1a': [{'level_2a': 99},
                                {'level_2b': 'wayne'}],
                   'level_1b': 'some text'
                   }
        write_response = record_controller.write_record(stream_id, payload)
        record_id = write_response.json()['recordId']

        read_response = record_controller.read_record(stream_id, record_id, False)
        assert len(read_response.json()) == 1
        assert read_response.json()[0]['dataPayload']['level_1b'] == 'some text'

        ## Cleanup
        stream_controller.delete_stream(stream_id)
