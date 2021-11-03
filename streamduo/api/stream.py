class Stream:
    def __init__(self, client):
        self.client = client

    def create_stream(self, stream_display_name):
        request_body = {'displayName': stream_display_name}
        return self.client.call_api('POST',
                                    "/stream",
                                    body=request_body)

    def get_stream(self, stream_id):
        return self.client.call_api('GET',
                                    f"/stream/{stream_id}")

    def delete_stream(self, stream_id):
        return self.client.call_api('DELETE',
                                    f"/stream/{stream_id}")

    def add_new_machine_client_to_stream(self, stream_id, client_display_name, is_producer=False, is_consumer=False ):
        body = {'actorDisplayName': client_display_name,
                'isProducer': is_producer,
                'isConsumer': is_consumer,
                'actorType': 'CLIENT'
                }
        return self.client.call_api('POST',
                                    f"/stream/{stream_id}/permissions",
                                    body=body)

    def remove_machine_client_from_stream(self, stream_id, client_id ):
        body = {'actorId': client_id
                }
        return self.client.call_api('DELETE',
                                    f"/stream/{stream_id}/permissions",
                                    body=body)