import json
import os
import pprint
from unittest import TestCase

from streamduo.client import Client
from streamduo.models.batch_data import BatchData
from streamduo.api.batch import BatchController
from streamduo.models.schema import SchemaType


class TestBatch(TestCase):

    def setUp(self) -> None:
        self.api_client = Client(os.getenv('AUTH_CLIENT_ID'), os.getenv('AUTH_CLIENT_SECRET'))

    def test_init_batch(self):
        display_name = 'batch_test_stream'
        stream_controller = self.api_client.get_stream_controller()
        new_stream_id = stream_controller.create_stream(display_name).json()['streamId']

        batch_controller = self.api_client.get_batch_controller()
        FILE_SIZE = 1024 * 1024 * 100  # 1GB
        big_file = "bigfile.dat"
        # multiply file
        with open(big_file, 'wb') as out_file:
            out_file.write(os.urandom(FILE_SIZE))

        resp = batch_controller.send_batch_init(stream_id=new_stream_id, file_path=big_file)
        batch_data = BatchData(**resp.json())
        assert len(batch_data.outstandingParts.keys()) == 20
        assert batch_data.streamSchema == None
        assert batch_data.requires_validation() == False

        ## Add schema to stream
        schema_controller = self.api_client.get_schema_controller()
        with open("car_schema.json", 'r') as file:
            car_schema = json.load(file)
        create_schema_response1 = schema_controller.create_schema(stream_id=new_stream_id,
                                                                  schema=car_schema, schema_type=SchemaType.JSON)
        new_schema_id = create_schema_response1.json()['schemaId']

        ## Set Active Schema
        set_active_response = schema_controller.set_active_schema(stream_id=new_stream_id, schema_id=new_schema_id)

        ## Create new Req
        resp = batch_controller.send_batch_init(stream_id=new_stream_id, file_path=big_file)
        batch_data = BatchData(**resp.json())
        assert len(batch_data.outstandingParts.keys()) == 20
        assert batch_data.requires_validation() == True
        assert batch_data.get_stream_schema().get_schema()['$id'] == 'https://example.com/object1644429127.json'

        ## Cleanup
        stream_controller.delete_stream(new_stream_id)

    def test_send_part(self):
        display_name = 'batch_test_stream'
        stream_controller = self.api_client.get_stream_controller()
        new_stream_id = stream_controller.create_stream(display_name).json()['streamId']

        batch_controller = self.api_client.get_batch_controller()
        FILE_SIZE = 1024 * 1024 * 100  # 1GB
        big_file = "bigfile.dat"
        # multiply file
        with open(big_file, 'wb') as out_file:
            out_file.write(os.urandom(FILE_SIZE))

        resp = batch_controller.send_batch_init(stream_id=new_stream_id, file_path=big_file)
        batch_data = BatchData(**resp.json())
        part_bin = BatchController.get_part_binary(file_path=big_file, part_number=5)
        ## Send part 5
        batch_data_resp = batch_controller.send_batch_part(batch_data=batch_data, part_number=5,
                                                           binary_payload=part_bin)
        batch_data_2 = BatchData(**batch_data_resp.json())
        pprint.pprint(batch_data_2.to_json())
        assert '5' not in batch_data_2.outstandingParts.keys()

        ## Cleanup
        stream_controller.delete_stream(new_stream_id)

    def test_full_file(self):
        display_name = 'batch_test_stream_full'
        stream_controller = self.api_client.get_stream_controller()
        new_stream_id = stream_controller.create_stream(display_name).json()['streamId']

        batch_controller = self.api_client.get_batch_controller()
        FILE_SIZE = 1024 * 1024 * 20  # 20MB
        big_file = "bigfile.dat"
        # multiply file
        with open(big_file, 'wb') as out_file:
            out_file.write(os.urandom(FILE_SIZE))

        batch_data = batch_controller.send_file(stream_id=new_stream_id, file_path=big_file)
        assert len(batch_data.outstandingParts.keys()) == 0
        ## Cleanup
        stream_controller.delete_stream(new_stream_id)

    def test_full_file_schema(self):
        display_name = 'batch_test_stream_full_schema'
        stream_controller = self.api_client.get_stream_controller()
        new_stream_id = stream_controller.create_stream(display_name).json()['streamId']

        ## Add schema to stream
        schema_controller = self.api_client.get_schema_controller()
        with open("car_schema.json", 'r') as file:
            car_schema = json.load(file)
        create_schema_response1 = schema_controller.create_schema(stream_id=new_stream_id,
                                                                  schema=car_schema, schema_type=SchemaType.JSON)
        new_schema_id = create_schema_response1.json()['schemaId']

        ## Set Active Schema
        schema_controller.set_active_schema(stream_id=new_stream_id, schema_id=new_schema_id)

        ## Send Good File
        batch_controller = self.api_client.get_batch_controller()
        batch_data = batch_controller.send_file(stream_id=new_stream_id, file_path="../test_data/car_sales.csv")
        assert len(batch_data.outstandingParts.keys()) == 0


        ## Send Bad File
        FILE_SIZE = 1024 * 1024 * 20  # 20MB
        big_file = "bigfile.csv"
        # multiply file
        with open(big_file, 'w') as out_file:
            out_file.write('bad data')


        #UnicodeDecodeError, TypeError
        batch_data = batch_controller.send_file(stream_id=new_stream_id, file_path=big_file)
        assert len(batch_data.outstandingParts.keys()) == 0
        ## Cleanup
        stream_controller.delete_stream(new_stream_id)