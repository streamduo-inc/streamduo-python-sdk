class Actor:
    def __init__(self, client):
        self.client = client

    def get_machine_client(self, machine_client_id):
        return self.client.call_api('GET', f"/client/{machine_client_id}")

    def create_machine_client(self, client_display_name, client_description):
        body = {'clientDisplayName':client_display_name,
                'clientDescription': client_description}
        return self.client.call_api('POST',
                                    "/client",
                                    body=body)

    def delete_machine_client(self, client_id):
        return self.client.call_api('DELETE',
                                    f"/client/{client_id}")
