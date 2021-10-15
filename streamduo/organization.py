import requests
import json

def put_new_organization(auth_manager, orgDomain, user):
    org = {
        'organizationDomain': orgDomain,
        'users': [user]
    }
    put_response = requests.post(f"{auth_manager.ENDPOINT_BASE_URL}/organization",
                                   headers=auth_manager.header,
                                   json=org)
    return json.loads(put_response.content)

def get_organization(auth_manager, organization_id):
    get_response = requests.get(f"{auth_manager.ENDPOINT_BASE_URL}/organization/{organization_id}",
                                   headers=auth_manager.header)
    return json.loads(get_response.content)

def add_user(auth_manager, organization_id, new_user):
    req = {
      "userAction": "ADD",
      "userId": new_user
    }
    add_response = requests.post(f"{auth_manager.ENDPOINT_BASE_URL}/organization/{organization_id}/update",
                                 headers=auth_manager.header,
                                 json=req)
    return json.loads(add_response.content)

def delete_organization(auth_manager, organization_id):
    get_response = requests.delete(f"{auth_manager.ENDPOINT_BASE_URL}/organization/{organization_id}",
                                   headers=auth_manager.header)
    return get_response.text
