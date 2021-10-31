import requests
import json
def put_stream(auth_manager, display_name):
    stream = {
        'displayName': display_name
    }

    create_stream_response = requests.post(f"{auth_manager.ENDPOINT_BASE_URL}/stream",
                                           headers=auth_manager.header,
                                           json=stream)
    return json.loads(create_stream_response.content)

def get_stream(auth_manager, stream_id):
    get_response = requests.get(f"{auth_manager.ENDPOINT_BASE_URL}/stream/{stream_id}",
                                   headers=auth_manager.header)
    print(get_response)
    if len(get_response.content) == 0:
        return None
    return json.loads(get_response.content)

def delete_stream(auth_manager, stream_id):
    get_response = requests.delete(f"{auth_manager.ENDPOINT_BASE_URL}/stream/{stream_id}",
                                   headers=auth_manager.header)
    return get_response.text

def add_new_client_id(auth_manager, client_name, stream_id, role):
    client_request = {
        'actorDisplayName': client_name,
        'isConsumer': False,
        'isProducer': False
    }
    if role == 'PRODUCER':
        client_request['isProducer'] = True
    if role == 'CONSUMER':
        client_request['isConsumer'] = True

    create_response = requests.post(f"{auth_manager.ENDPOINT_BASE_URL}/stream/{stream_id}/add/client/new",
                                   headers=auth_manager.header,
                                   json=client_request)
    return json.loads(create_response.content)

