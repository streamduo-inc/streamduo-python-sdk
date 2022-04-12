from streamduo.models.batch_init_request import BatchInitRequest
import hashlib
import os

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
                part_data = {"partNumber": part_number,
                             "partHashValue": hashlib.md5(data).hexdigest()}
                batch_init_request.partList.append(part_data)
                part_number = part_number + 1

        batch_init_request.hashValue = md5.hexdigest()
        batch_init_request.fileName = os.path.basename(file_path)
        batch_init_request.totalParts = part_number
        return batch_init_request

    def upload_binary(self, stream_id, file_path, BUF_SIZE):
        request_object = BatchController.construct_batch_init_request(file_path=file_path, BUF_SIZE=BUF_SIZE)
        return self.client.call_api('POST',
                                    f"/stream/{stream_id}/batch/init",
                                    body=request_object.to_json())
