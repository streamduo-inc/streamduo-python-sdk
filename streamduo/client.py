import requests

def delete_client(auth_manager, client_id):
    get_response = requests.delete(f"{auth_manager.ENDPOINT_BASE_URL}/client/{client_id}",
                                   headers=auth_manager.header)
    return get_response.text