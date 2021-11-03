class Health:
    def __init__(self, client):
        self.client = client

    def check_health(self):
        return self.client.call_api('GET', "/health")