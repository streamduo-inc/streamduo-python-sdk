from time import sleep
from unittest import TestCase
import os

from requests import HTTPError

from streamduo.client import Client
import pandas as pd

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

    def test_write_record_pandas(self):
        display_name = 'test_stream'
        stream_controller = Client(os.getenv('AUTH_CLIENT_ID'), os.getenv('AUTH_CLIENT_SECRET')).get_stream_controller()
        stream_request_result = stream_controller.create_stream(display_name)
        stream_id = stream_request_result.json()['streamId']

        record_controller = Client(os.getenv('AUTH_CLIENT_ID'), os.getenv('AUTH_CLIENT_SECRET')).get_record_controller()

        car_sales = pd.read_csv("car_sales.csv")
        for index, row in car_sales.iterrows():
            write_response = record_controller.write_record(stream_id, row.to_json())

        read_records_response = record_controller.read_unread_records(stream_id=stream_id, mark_as_read=False,
                                                                      record_count=100)
        assert len(read_records_response.json()) == 10

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

    def test_simple_unread_records(self):
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

        read_one_response = record_controller.read_record(stream_id, record_id_2, True)

        read_unread_response = record_controller.simple_read_unread_records(stream_id)
        assert len(read_unread_response.json()) == 2

        #Try again, should be all read and no results
        read_unread_response = record_controller.simple_read_unread_records(stream_id)
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


    def test_add_to_record_id(self):
        display_name = 'test_stream'
        stream_controller = Client(os.getenv('AUTH_CLIENT_ID'), os.getenv('AUTH_CLIENT_SECRET')).get_stream_controller()
        stream_request_result = stream_controller.create_stream(display_name)
        stream_id = stream_request_result.json()['streamId']

        record_controller = Client(os.getenv('AUTH_CLIENT_ID'), os.getenv('AUTH_CLIENT_SECRET')).get_record_controller()
        record_id = '111111111'

        payload = {
            'Part Description': 'Widget A',
            'Price': 10.00,
            'Inventory': 20000
        }

        write_response = record_controller.write_record(stream_id, payload, record_id=record_id)

        #write again to same ID
        payload = {
            'Part Description': 'Widget A',
            'Price': 11.00,
            'Inventory': 15000
        }
        write_response2 = record_controller.write_record(stream_id, payload, record_id=record_id)

        assert write_response2.json()['recordId'] == record_id

        ##get a record ID returns 2
        read_response = record_controller.read_record(stream_id, record_id, False)
        assert len(read_response.json()) == 1
        assert read_response.json()[0]['dataPayload']['Inventory'] == 15000

        read_hist_response = record_controller.read_record_hist(stream_id=stream_id, record_id=record_id, count=3, mark_as_read=True)
        assert len(read_hist_response.json()) == 2


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
        self.assertRaises(HTTPError, record_controller.write_record, "madeupsstreamid", payload)


