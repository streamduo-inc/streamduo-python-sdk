from streamduo.validate import Validator, validate_schema
class SchemaController:
    """
    Class for managing interaction with the /schema endpoints
    """
    def __init__(self, client):
        """
        Constructor, must be instantiated with a client to provide auth support
        :param client: (Client) client object
        """
        self.client = client

    def create_schema(self, schema, schema_type):
        """
        Creates a new Schema
        :param schema: (DICT) Desired schema
        :return: (Requests Response) Response from API call, Body of response is a Schema Object
        """
        validate_schema(schema)
        request_body = {'schema': schema,
                        'schemaType': schema_type}
        return self.client.call_api('POST',
                                    "/schemas",
                                    body=request_body)

    def delete_schema(self, schema_id, schema_version):
        """
        Deletes a Schema
        :param schema_id: (STRING) Desired schema to delete
        :param schema_version: (STRING) Desired version of schema to delete
        :return: (Requests Response) Response from API call, Body of response is null.
        """
        return self.client.call_api('DELETE',
                                    f"/schemas/{schema_id}/versions/{schema_version}")
