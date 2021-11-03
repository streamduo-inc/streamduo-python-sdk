class Stream:
    def __init__(self, client):
        self.client = client

    def create_stream(self, stream_display_name):
        request_body = {'displayName': stream_display_name}
        return self.client.call_api('POST', "/stream", body=request_body)

    def get_stream(self, stream_id):
        return self.client.call_api('GET', f"/stream/{stream_id}")

    def delete_stream(self, stream_id):
        return self.client.call_api('DELETE', f"/stream/{stream_id}")