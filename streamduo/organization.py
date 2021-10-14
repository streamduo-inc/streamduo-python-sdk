import requests

def put_new_organization(auth_manager):
    org = {
        'organizationDomain': 'dtps.io',
        'users': ['steve']
    }
    put_response = requests.post(f"{auth_manager.ENDPOINT_BASE_URL}/organization",
                                   headers=auth_manager.header,
                                   json=org)
    return put_response

def get_organization(auth_manager, organization_id):
    get_response = requests.get(f"{auth_manager.ENDPOINT_BASE_URL}/organization/{organization_id}",
                                   headers=auth_manager.header)
    return get_response.content

def add_user(auth_manager, organization_id, new_user):
    req = {
      "organizationId": organization_id,
      "userAction": "ADD",
      "userId": new_user
    }
    add_response = requests.post(f"{auth_manager.ENDPOINT_BASE_URL}/organization/update",
                                 headers=auth_manager.header,
                                 json=req)
    return add_response

def delete_organization(auth_manager, organization_id):
    get_response = requests.delete(f"{auth_manager.ENDPOINT_BASE_URL}/organization/{organization_id}",
                                   headers=auth_manager.header)
    return get_response.text
