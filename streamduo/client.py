import requests

def delete_client(auth_manager, client_id):
    get_response = requests.delete(f"{auth_manager.ENDPOINT_BASE_URL}/client/{client_id}",
                                   headers=auth_manager.header)
    return get_response.text


def cleanup_clients(auth_manager):
    baseURI = "https://dev-v475zrua.us.auth0.com/api/v2/clients"
    clients = requests.get(baseURI,
                           headers=auth_manager.header)
    for c in clients.json():
        if 'app_type' not in c and c['name'] in ['SuperClient','client_id_1', 'client_id_2', 'client_id_3' ]:
            print(c['name'], c['client_id'])
            d = requests.delete(f"{baseURI}/{c['client_id']}",
                           headers=auth_manager.header)
