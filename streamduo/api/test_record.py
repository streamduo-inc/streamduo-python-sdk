from time import sleep
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


    def test_unread_records(self):
        display_name = 'test_stream'
        stream_controller = Client(os.getenv('AUTH_CLIENT_ID'),
                                   os.getenv('AUTH_CLIENT_SECRET')).get_stream_controller()
        stream_request_result = stream_controller.create_stream(display_name)
        stream_id = stream_request_result.json()['streamId']

        record_controller = Client(os.getenv('AUTH_CLIENT_ID'),
                                   os.getenv('AUTH_CLIENT_SECRET')).get_record_controller()
        payload_1 = {'payload': 1}

        payload_2 = {'payload': 2}

        payload_3 = {'payload': 3}

        record_id_1 = record_controller.write_record(stream_id, payload_1).json()['recordId']
        record_id_2 = record_controller.write_record(stream_id, payload_2).json()['recordId']
        record_id_3 = record_controller.write_record(stream_id, payload_3).json()['recordId']

        read_unread_response = record_controller.read_unread_records(stream_id, False, 5)
        assert len(read_unread_response.json()) == 3

        read_one_response = record_controller.read_record(stream_id,record_id_2, True)

        read_unread_response = record_controller.read_unread_records(stream_id, True, 5)
        assert len(read_unread_response.json()) == 2

        read_unread_response = record_controller.read_unread_records(stream_id, False, 5)
        assert len(read_unread_response.json()) == 0

        ## Cleanup
        stream_controller.delete_stream(stream_id)

    def test_last_n_records(self):
        display_name = 'test_stream'
        stream_controller = Client(os.getenv('AUTH_CLIENT_ID'),
                                   os.getenv('AUTH_CLIENT_SECRET')).get_stream_controller()
        stream_request_result = stream_controller.create_stream(display_name)
        stream_id = stream_request_result.json()['streamId']

        record_controller = Client(os.getenv('AUTH_CLIENT_ID'),
                                   os.getenv('AUTH_CLIENT_SECRET')).get_record_controller()
        payload_1 = {'payload': 1}

        payload_2 = {'payload': 2}

        payload_3 = {'payload': 3}

        record_id_1 = record_controller.write_record(stream_id, payload_1).json()['recordId']
        record_id_2 = record_controller.write_record(stream_id, payload_2).json()['recordId']
        record_id_3 = record_controller.write_record(stream_id, payload_3).json()['recordId']

        read_unread_response = record_controller.read_last_n_records(stream_id, False, 2)
        assert len(read_unread_response.json()) == 2
        record_list = []
        for r in read_unread_response.json():
            record_list.append(r['recordId'])
        assert record_id_3 in record_list
        assert record_id_2 in record_list
        assert record_id_1 not in record_list

        read_unread_response = record_controller.read_last_n_records(stream_id, False, 10)
        assert len(read_unread_response.json()) == 3
        record_list = []
        for r in read_unread_response.json():
            record_list.append(r['recordId'])
        assert record_id_3 in record_list
        assert record_id_2 in record_list
        assert record_id_1 in record_list

        ## Cleanup
        stream_controller.delete_stream(stream_id)

    def test_read_since_timestamp(self):
        display_name = 'test_stream'
        stream_controller = Client(os.getenv('AUTH_CLIENT_ID'),
                                   os.getenv('AUTH_CLIENT_SECRET')).get_stream_controller()
        stream_request_result = stream_controller.create_stream(display_name)
        stream_id = stream_request_result.json()['streamId']

        record_controller = Client(os.getenv('AUTH_CLIENT_ID'),
                                   os.getenv('AUTH_CLIENT_SECRET')).get_record_controller()
        payload_1 = {'payload': 1}
        payload_2 = {'payload': 2}
        payload_3 = {'payload': 3}

        record_1 = record_controller.write_record(stream_id, payload_1).json()
        sleep(3)
        record_2 = record_controller.write_record(stream_id, payload_2).json()
        sleep(3)
        record_3 = record_controller.write_record(stream_id, payload_3).json()

        read_timestamp_response = record_controller.read_records_since_timestamp(stream_id, record_2['recordTimeStampISO'], False, 5)
        assert len(read_timestamp_response.json()) == 1
        record_list = []
        for r in read_timestamp_response.json():
            record_list.append(r['recordId'])
        assert record_1['recordId'] not in record_list
        assert record_2['recordId'] not in record_list
        assert record_3['recordId'] in record_list

        #Trim timestamp to the second
        read_timestamp_response = record_controller.read_records_since_timestamp(stream_id, record_2['recordTimeStampISO'][:19], False, 5)
        assert len(read_timestamp_response.json()) == 2
        record_list = []
        for r in read_timestamp_response.json():
            record_list.append(r['recordId'])
        assert record_1['recordId'] not in record_list
        assert record_2['recordId'] in record_list
        assert record_3['recordId'] in record_list

        ## Cleanup
        stream_controller.delete_stream(stream_id)

    def test_write_record_errors(self):
        record_controller = Client(os.getenv('AUTH_CLIENT_ID'),
                                   os.getenv('AUTH_CLIENT_SECRET')).get_record_controller()

        #stream does not exist
        payload = {'level_1a': [{'level_2a': 99},
                                {'level_2b': 'wayne'}],
                   'level_1b': 'some text'
                   }
        write_response = record_controller.write_record("madeupsstreamid", payload)
        print(write_response)
        assert write_response.status_code == 401


