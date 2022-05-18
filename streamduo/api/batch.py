import tempfile

from streamduo.api.key import KeyController
from streamduo.models.batch_data import BatchData
from streamduo.models.batch_init_request import BatchInitRequest
import hashlib
import os
import base64

from streamduo.models.schema import SchemaType

from streamduo.models.schema import FileType
from streamduo.validators.json_schema import JsonValidator
from streamduo.validators.great_expectations_schema import GreatExepectationsValidator


class BatchController:
    """
    Provides methods for interacting with the `/batch` endpoints
    """
    BUFFER_SIZE = 1024 * 1024 * 5  # 5 MB

    def __init__(self, client):
        self.client = client

    @staticmethod
    def construct_batch_init_request(file_path, file_name_override=None):
        """
        constructs the payload for the initiate batch file upload request
        :param file_path: (STRING) path to file for upload.
        :param file_name_override: (STRING) optional override for file name
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
        if file_name_override:
            file_name_metadata = file_name_override
        else:
            file_name_metadata = file_path
        batch_init_request.fileName = os.path.basename(file_name_metadata)
        file_name, file_extension = os.path.splitext(file_name_metadata)
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

    def send_batch_init(self, stream_id, file_path, file_path_override=None):
        """
        Sends a Batch initiation request to the API.
        :param stream_id: (STRING) Stream ID file will be uploaded to.
        :param file_path: (STRING) Path to file being uploaded.
        :param file_path_override: (STRING) optional overrride for file path
        :return:
        """
        request_object = BatchController.construct_batch_init_request(file_path=file_path,
                                                                      file_name_override=file_path_override)
        return self.client.call_api('POST',
                                    f"/stream/{stream_id}/batch/init",
                                    body=request_object.to_json())

    def send_batch_part(self, batch_data, part_number, binary_payload):
        """
        Sends a part/chunk of the binary data to the upload-part endpoint
        :param batch_data: (streamduo.models.BatchData) batch metadata object
        :param part_number: (INT) part number of data payload
        :param binary_payload: (BYTES) binary data payload for part/chunk
        :return: (requests.response) API response object
        """
        file_payload = {'file': binary_payload}
        return self.client.call_api('POST',
                                    f"/stream/{batch_data.streamId}/batch/{batch_data.batchId}/upload-part/{part_number}",
                                    files=file_payload)

    def send_file(self, stream_id, file_path):
        """
        High level function for sending a file to a streamduo stream. function handles:
        1. Data Validation
        2. Encryption
        3. Chunking/multipart uploading

        :param stream_id: (STRING) target stream ID.
        :param file_path:  (STRING) file path to file to be uploaded.
        :return: (streamduo.models.BatchData) batch metadata object
        """
        ## init req
        batch_data = BatchData(**self.send_batch_init(stream_id=stream_id,
                                                      file_path=file_path).json())
        ## validate
        ## CSV w. JSON Schema
        if batch_data.requires_validation() \
                and batch_data.get_file_type() == FileType.CSV \
                and batch_data.get_stream_schema().get_schema_type() == SchemaType.JSON:
            val = JsonValidator()
            val.set_schema(batch_data.get_stream_schema().get_schema())
            val.validate_csv(file_path)

        ## CSV w. GE Schema
        if batch_data.requires_validation() \
                and batch_data.get_file_type() == FileType.CSV \
                and batch_data.get_stream_schema().get_schema_type() == SchemaType.GREAT_EXPECTATIONS:
            val = GreatExepectationsValidator()
            val.set_schema(batch_data.get_stream_schema().get_schema())
            val.validate_csv(file_path)

        ## Encryption
        if batch_data.requires_encryption():
            with tempfile.NamedTemporaryFile() as tmp:
                KeyController.encrypt_file(key_string=batch_data.get_public_key_value(), source_file_path=file_path,
                                           destination_file_path=tmp.name)
                batch_data = BatchData(**self.send_batch_init(stream_id=stream_id,
                                                              file_path=tmp.name,
                                                              file_path_override=file_path).json())
                return self.send_chunks(batch_data=batch_data, file_path=tmp.name)

        else:
            return self.send_chunks(batch_data=batch_data, file_path=file_path)

    def send_chunks(self, batch_data, file_path) -> BatchData:
        """
        high level function for chunking up a binary file and sending to streamduo
        :param batch_data: (streamduo.models.BatchData) batch metadata object
        :param file_path: (STRING) path to file which is being sent.
        :return: (streamduo.models.BatchData) batch metadata object
        """
        # send via loop chunks
        with open(file_path, 'rb') as out_file:
            while len(batch_data.outstandingParts.keys()) > 0:
                part_number = next(iter(batch_data.outstandingParts.items()))[0]
                data = BatchController.get_part_binary(file_path=file_path, part_number=part_number)
                # send data
                batch_data = BatchData(**self.send_batch_part(batch_data=batch_data,
                                                              part_number=part_number, binary_payload=data).json())
        return batch_data

    def get_part(self, stream_id, batch_id, part_number) -> bytes:
        """
        Downloads a specific part/chunk of a larger file from the streamduo stream
        :param stream_id: (STRING) target stream ID
        :param batch_id: (STRING) target batch ID
        :param part_number: (INT) part number
        :return: (BYTES) data payload of part/chunk
        """

        resp = self.client.call_api('GET',
                                    f"/stream/{stream_id}/batch/{batch_id}/get-part/{part_number}")
        return resp.content

    def get_batch(self, stream_id: str, batch_id: str, destination_filepath: str, decryption_key: str = None):
        """
        High level function for retreving a complete batch file from streamduo.
        function includes decryption and reconstructing from parts/chunks.
        :param stream_id: (STRING) target stream ID
        :param batch_id: (STRING) target batch ID
        :param destination_filepath: (STRING) destination file path to save file to
        :param decryption_key: (STRING) private key for decryption
        :return: None
        """
        ## get batchdata
        batch_data = self.get_batch_metadata(stream_id=stream_id, batch_id=batch_id)
        outstanding_parts = batch_data.hashes.copy()
        with tempfile.TemporaryDirectory() as td:
            while len(outstanding_parts.keys()) > 0:
                part_number = next(iter(outstanding_parts.items()))[0]
                file_name = os.path.join(td, f"{stream_id}-{batch_id}-{str(part_number)}.part")
                part_data = self.get_part(stream_id=stream_id, batch_id=batch_id, part_number=part_number)
                ## validate part download
                if outstanding_parts[part_number] != base64.b64encode(hashlib.md5(part_data).digest()).decode():
                    raise ValueError
                with open(file_name, 'wb') as fh:
                    fh.write(part_data)
                del outstanding_parts[part_number]
            ## Compile final file
            final_file_tmp = os.path.join(td, f"{stream_id}-{batch_id}.final")
            with open(final_file_tmp, 'wb') as final_file:
                for pn in batch_data.hashes.keys():
                    with open(os.path.join(td, f"{stream_id}-{batch_id}-{str(pn)}.part"), 'rb') as part_file:
                        final_file.write(part_file.read())
            if batch_data.requires_encryption():
                KeyController.decrypt_file(source_file_path=final_file_tmp,
                                           destination_file_path=destination_filepath,
                                           key_string=decryption_key)
            else:
                os.rename(final_file_tmp, destination_filepath)

    def get_batch_metadata(self, stream_id: str, batch_id: str) -> BatchData:
        """
        Method for downloading batch metadata
        :param stream_id: (STRING) target stream ID
        :param batch_id: (STRING) target batch ID
        :return: (streamduo.models.BatchData) batch metadata object
        """
        resp = self.client.call_api('GET', f"/stream/{stream_id}/batch/{batch_id}")
        return BatchData(**resp.json())

    def get_unread_batches(self, stream_id: str):
        """
        Method for getting the unread batch records
        :param stream_id: (STRING) target stream ID
        :return: (DICT) list of unread records
        """
        resp = self.client.call_api('GET', f"/stream/{stream_id}/batch/unread")
        return resp.json()

    def mark_batch_read(self, stream_id: str, batch_id: str) -> bool:
        """
        Method for marking a specific batch as having been read
        :param stream_id: (STRING) target stream ID
        :param batch_id: (STRING) target batch ID
        :return: (BOOL) success status
        """
        resp = self.client.call_api('POST', f"/stream/{stream_id}/record/{batch_id}/mark-read")
        return resp.status_code == 200
