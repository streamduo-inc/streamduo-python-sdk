class ActorController:
    """
    Provides methods for interacting with the `/client` endpoints
    Machine 'clients' are managed via this class
    """
    def __init__(self, client):
        self.client = client

    def get_machine_client(self, machine_client_id):
        """
        Get the details of a machine client ID
        :param machine_client_id: (String) machine client ID
        :return: (Requests Response) response of the API call, body will be a Client object
        """
        return self.client.call_api('GET', f"/client/{machine_client_id}")

    def create_machine_client(self, client_display_name, client_description):
        """
        Creates a new machine client
        :param client_display_name: (String) Desired display name for client
        :param client_description: (String) Desired description for client
        :return:  (Requests Response) response of the API call, body will be a Client object
        """
        body = {'clientDisplayName':client_display_name,
                'clientDescription': client_description}
        return self.client.call_api('POST',
                                    "/client",
                                    body=body)

    def delete_machine_client(self, client_id):
        """
        Deletes a machine client
        :param client_id: (String) Client ID to delete
        :return: :return:  (Requests Response) response of the API call, body will be empty
        """
        return self.client.call_api('DELETE',
                                    f"/client/{client_id}")

    def get_user(self):
        return self.client.call_api('GET', "/user")