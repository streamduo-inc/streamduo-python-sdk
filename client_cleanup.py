import os
import requests

from streamduo.auth import AuthManager


if __name__ == "__main__":
    auth_manager = AuthManager(os.getenv("AUTH0_API_CLIENT_ID"),
                               os.getenv("AUTH0_API_CLIENT_SECRET"))
    auth_manager.AUTH_URL = "https://dev-v475zrua.us.auth0.com/oauth/token"
    auth_manager.token_req_payload['audience'] = 'https://dev-v475zrua.us.auth0.com/api/v2/'
    auth_manager.token_req_payload['grant_type'] = 'client_credentials'
    clients = requests.get("https://dev-v475zrua.us.auth0.com/api/v2/clients",
                                   headers=auth_manager.get_header())
    cnt = 0
    for c in clients.json():
        if(c['name'] in ['client_id_1', 'client_id_2', 'client_id_3']):
            get_grant = requests.get(f"https://dev-v475zrua.us.auth0.com/api/v2/client-grants?client_id={c['client_id']}",
                                      headers=auth_manager.get_header())
            print("---")
            for g in get_grant.json():
                print (g['id'])
                del_grant = requests.delete(
                    f"https://dev-v475zrua.us.auth0.com/api/v2/client-grants/{g['id']}",
                    headers=auth_manager.get_header())
                print (del_grant.content)
            print("---")

            del_out = requests.delete(f"https://dev-v475zrua.us.auth0.com/api/v2/clients/{c['client_id']}",
                         headers=auth_manager.get_header())
            print(del_out.content)
            print(c['name'], c['client_id'])
            cnt = cnt + 1
