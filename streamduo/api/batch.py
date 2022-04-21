from streamduo.models.batch_init_request import BatchInitRequest
import hashlib
import os
import base64

class BatchController:
    """
    Provides methods for interacting with the `/batch` endpoints
    """

    def __init__(self, client):
        self.client = client

    @staticmethod
    def construct_batch_init_request(file_path, BUF_SIZE):
        # split file
        # construct request
        batch_init_request = BatchInitRequest()
        part_number = 1
        # multiply file
        with open(file_path, 'rb') as out_file:
            md5 = hashlib.md5()
            while True:
                data = out_file.read(BUF_SIZE)
                if not data:
                    break
                # update file Hash
                md5.update(data)
                # construct part data info
                batch_init_request.hashes[part_number] = base64.b64encode(hashlib.md5(data).digest()).decode()
                part_number = part_number + 1

        batch_init_request.hashValue = base64.b64encode(md5.digest()).decode()
        batch_init_request.fileName = os.path.basename(file_path)
        batch_init_request.totalParts = part_number
        return batch_init_request

    def send_batch_init(self, stream_id, file_path, BUF_SIZE):
        request_object = BatchController.construct_batch_init_request(file_path=file_path, BUF_SIZE=BUF_SIZE)
        return self.client.call_api('POST',
                                    f"/stream/{stream_id}/batch/init",
                                    body=request_object.to_json())

    def send_batch_part(self, batch_data, part_number, binary_payload):
        #Validate Hash
        #Construct payload
        file_payload = {'file': binary_payload}
        #send
        return self.client.call_api('POST',
                                    f"/stream/{batch_data.streamId}/batch/{batch_data.batchId}/upload-part/{part_number}",
                                    files=file_payload)

    @staticmethod
    def get_part_binary(file_path, part_number, BUF_SIZE):
        part_counter = 1
        with open(file_path, 'rb') as out_file:
            while part_counter <= int(part_number):
                data = out_file.read(BUF_SIZE)
                # EOF
                if not data:
                    break
                part_counter = part_counter + 1
            return data



    def send_file(self, batch_data, file_path, BUF_SIZE):
        #loop chunks
        with open(file_path, 'rb') as out_file:
            while len(batch_data.outstandingParts.keys()) > 0:
                part_number = next(iter(batch_data.outstandingParts.items()))[0]
                data = BatchController.get_part_binary(file_path=file_path, part_number=part_number, BUF_SIZE=BUF_SIZE)
                #send data
                batch_data = self.send_batch_part(batch_data=batch_data, part_number=part_number, binary_payload=data)


