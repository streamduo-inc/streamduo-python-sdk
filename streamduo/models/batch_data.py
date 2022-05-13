from nacl.public import SealedBox

from streamduo.api.key import KeyController
from streamduo.models.schema import Schema, FileType


class BatchData:
    """
    Class for creating batch file inti request objects.
    Creating the request with a class helps ensure that the request body
    conforms to the requirements on the API side.
    """

    def __init__(self, batchId, streamId, fileName, hashes, hashValue, outstandingParts, serverSideValidation=None, totalParts=None, fileType=None, streamSchema=None, streamPublicKey=None):
        """
         Constructor
         """
        self.batchId = batchId
        self.streamId = streamId
        self.fileName = fileName
        self.hashes = hashes
        self.hashValue = hashValue
        self.fileType = fileType
        self.outstandingParts = outstandingParts
        self.serverSideValidation = serverSideValidation
        self.totalParts = totalParts
        self.streamSchema = streamSchema
        self.streamPublicKey = streamPublicKey

    def to_json(self):
        return self.__dict__

    def get_stream_schema(self):
        return Schema(**self.streamSchema)

    def get_public_key_value(self):
        return self.streamPublicKey['publicKeyValue']

    def get_file_type(self):
        try:
            return FileType[self.fileType]
        except KeyError:
            return None

    def requires_validation(self):
        return self.streamSchema is not None

    def requires_encryption(self):
        return self.streamPublicKey is not None

