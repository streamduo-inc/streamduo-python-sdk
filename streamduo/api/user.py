class User:
    def __init__(self, client):
        self.client = client

    def get_user(self):
        return self.client.call_api('GET', "/user")