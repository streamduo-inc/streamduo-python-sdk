import requests
import json
def create_user(auth_manager):
    create_user_response = requests.post(f"{auth_manager.ENDPOINT_BASE_URL}/user",
                                           headers=auth_manager.header,
                                            json={})
    return json.loads(create_user_response.content)


def get_user(auth_manager):
    create_user_response = requests.get(f"{auth_manager.ENDPOINT_BASE_URL}/user",
                                         headers=auth_manager.header)
    return json.loads(create_user_response.content)

def get_health(auth_manager):
    create_user_response = requests.get(f"{auth_manager.ENDPOINT_BASE_URL}/health",
                                         headers=auth_manager.header)
    return json.loads(create_user_response.content)
