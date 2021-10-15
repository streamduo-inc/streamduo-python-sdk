import requests
import json
def put_stream(auth_manager, display_name, producer_org_id, consumer_org_id):
    stream = {
        'displayName': display_name,
        'producerOrganizationId': producer_org_id,
        'consumerOrganizationId': consumer_org_id
    }

    create_stream_response = requests.post(f"{auth_manager.ENDPOINT_BASE_URL}/stream",
                                           headers=auth_manager.header,
                                           json=stream)
    return json.loads(create_stream_response.content)

def get_stream(auth_manager, stream_id):
    get_response = requests.get(f"{auth_manager.ENDPOINT_BASE_URL}/stream/{stream_id}",
                                   headers=auth_manager.header)
    return json.loads(get_response.content)

def delete_stream(auth_manager, stream_id):
    get_response = requests.delete(f"{auth_manager.ENDPOINT_BASE_URL}/stream/{stream_id}",
                                   headers=auth_manager.header)
    return get_response.text

def update_stream_client_id(auth_manager, stream_id, client_id, role, action):
    stream_update = {
        'clientId': client_id,
        'streamUpdateRequestRole': role,
        'streamUpdateRequestAction': action
    }
    print(stream_update)
    update_response = requests.post(f"{auth_manager.ENDPOINT_BASE_URL}/stream/{stream_id}/update",
                                   headers=auth_manager.header,
                                   json=stream_update)
    return json.loads(update_response.content)