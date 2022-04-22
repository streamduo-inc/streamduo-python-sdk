class BatchInitRequest:
    """
    Class for creating batch file inti request objects.
    Creating the request with a class helps ensure that the request body
    conforms to the requirements on the API side.
    """

    def __init__(self):
        """
         Constructor
         """
        self.fileName = None
        self.hashes = {}
        self.hashValue = None
        self.fileType = None
        self.serverSideValidation = False
        self.totalParts = None

    def to_json(self):
        return self.__dict__