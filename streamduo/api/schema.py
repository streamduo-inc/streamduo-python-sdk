from streamduo.validators.json_schema import validate_schema
from streamduo.models.schema import Schema


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

    def create_schema(self, stream_id, schema, schema_type):
        """
        Creates a new Schema
        :param schema: (DICT) Desired schema
        :param stream_id: (STRING) stream to attach schema to
        :param schema_type (STRING) type of schema (JSON, AVRO, GREAT_EXPECTATIONS)
        :return: (Requests Response) Response from API call, Body of response is a Schema Object
        """
        validate_schema(schema)
        request_body = {'schema': schema,
                        'schemaType': schema_type.value}
        return self.client.call_api('POST',
                                    f"/streams/{stream_id}/schemas",
                                    body=request_body)

    def delete_schema(self, stream_id, schema_id):
        """
        Deletes a Schema
        :param schema_id: (STRING) Desired schema to delete
        :param stream_id: (STRING) Desired stream of schema to delete
        :return: (Requests Response) Response from API call, Body of response is null.
        """
        return self.client.call_api('DELETE',
                                    f"/streams/{stream_id}/schemas/{schema_id}/")

    def get_schema(self, stream_id, schema_id):
        """
        Gets a Schema
        :param schema_id: (STRING) Desired schema to get
        :param stream_id: (STRING) Desired stream of schema to delete
        :return: (Requests Response) Response from API call.
        """
        resp = self.client.call_api('GET',
                                    f"/streams/{stream_id}/schemas/{schema_id}/")
        schema = Schema(**resp.json())
        return schema

    def set_active_schema(self, stream_id, schema_id):
        """
        Sets the active schema on a stream
        :param stream_id: Desired stream to set Schema to
        :param schema_id: Desired schema ID to set active
        :return: (Requests Response) Response from API call.
        """
        request_body = {"schemaId": schema_id}
        return self.client.call_api('POST',
                                    f"/stream/{stream_id}/schemas/active",
                                    body=request_body)

