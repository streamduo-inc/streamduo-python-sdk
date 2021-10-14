import requests

def put_new_organization(auth_manager):
    org = {
        'organizationDomain': 'dtps.io',
        'users': ['steve']
    }
    table_response = requests.post(f"{auth_manager.ENDPOINT_BASE_URL}/organization",
                                   headers=auth_manager.header,
                                   json=org)
    print("xxx")
    print(table_response)
    return table_response

def get_organization(auth_manager, organization_id):
    table_response = requests.get(f"{auth_manager.ENDPOINT_BASE_URL}/organization/{organization_id}",
                                   headers=auth_manager.header)
    print(table_response.json())
    return table_response