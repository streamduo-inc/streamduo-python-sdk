from streamduo.models.batch_data import BatchData
from streamduo.models.batch_init_request import BatchInitRequest
import hashlib
import os
import base64

from streamduo.models.schema import SchemaType

from streamduo.models.schema import FileType
from streamduo.validators.json_schema import JsonValidator


class BatchController:
    """
    Provides methods for interacting with the `/batch` endpoints
    """
    BUFFER_SIZE = 1024 * 1024 * 5  # 5 MB

    def __init__(self, client):
        self.client = client

    @staticmethod
    def construct_batch_init_request(file_path):
        """
        constructs the payload for the initiate batch file upload request
        :param file_path: (STRING) path to file for upload.
        :return: (BatchInitRequest) object.
        """
        # construct request
        batch_init_request = BatchInitRequest()
        part_number = 1
        # break down chunks
        with open(file_path, 'rb') as out_file:
            full_file_md5 = hashlib.md5()
            while True:
                data = out_file.read(BatchController.BUFFER_SIZE)
                if not data:
                    break
                # update full file Hash
                full_file_md5.update(data)
                # add part hash as b64 to batch init req
                batch_init_request.hashes[part_number] = base64.b64encode(
                    hashlib.md5(data).digest()).decode()
                part_number = part_number + 1

        batch_init_request.hashValue = base64.b64encode(full_file_md5.digest()).decode()
        batch_init_request.fileName = os.path.basename(file_path)
        filename, file_extension = os.path.splitext(file_path)
        file_extension = file_extension.strip('.').upper()
        if file_extension in FileType._member_names_:
            batch_init_request.fileType = FileType[file_extension].value
        batch_init_request.totalParts = part_number
        return batch_init_request

    @staticmethod
    def get_part_binary(file_path, part_number):
        """
        returns the bytes for a particular "part number" of a file.
        :param file_path: (STRING) path to file for upload.
        :param part_number: (INT) part number to return
        :return: (BYTES) bytes of data corresponding to the file part.
        """
        part_counter = 1
        with open(file_path, 'rb') as out_file:
            while part_counter <= int(part_number):
                data = out_file.read(BatchController.BUFFER_SIZE)
                # EOF
                if not data:
                    break
                part_counter = part_counter + 1
            return data

    def send_batch_init(self, stream_id, file_path):
        """
        Sends a Batch initiation request to the API.
        :param stream_id: (STRING) Stream ID file will be uploaded to.
        :param file_path: (STRING) Path to file being uploaded.
        :return:
        """
        request_object = BatchController.construct_batch_init_request(file_path=file_path)
        return self.client.call_api('POST',
                                    f"/stream/{stream_id}/batch/init",
                                    body=request_object.to_json())

    def send_batch_part(self, batch_data, part_number, binary_payload):
        file_payload = {'file': binary_payload}
        return self.client.call_api('POST',
                                    f"/stream/{batch_data.streamId}/batch/{batch_data.batchId}/upload-part/{part_number}",
                                    files=file_payload)

    def send_file(self, stream_id, file_path):
        ## init req
        batch_data = BatchData(**self.send_batch_init(stream_id=stream_id,
                                                      file_path=file_path).json())

        ## CSV w. JSON Schema
        if batch_data.requires_validation() \
                and batch_data.get_file_type() == FileType.CSV \
                and batch_data.get_stream_schema().get_schema_type() == SchemaType.JSON:
            ## validate
            val = JsonValidator()
            val.set_schema(batch_data.get_stream_schema().get_schema())
            val.validate_csv(file_path)

        # send via loop chunks
        with open(file_path, 'rb') as out_file:
            while len(batch_data.outstandingParts.keys()) > 0:
                part_number = next(iter(batch_data.outstandingParts.items()))[0]
                data = BatchController.get_part_binary(file_path=file_path, part_number=part_number)
                # send data
                print(f"""sending part: {part_number}""")
                batch_data = BatchData(**self.send_batch_part(batch_data=batch_data,
                                                              part_number=part_number, binary_payload=data).json())
        return batch_data
