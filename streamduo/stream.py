from auth import *
import requests

def get_table_list(auth_manager):
    table_response = requests.get(f"{auth_manager.ENDPOINT_BASE_URL}/stream/list", headers=auth_manager.header)
    print(table_response)
    return table_response.json()

