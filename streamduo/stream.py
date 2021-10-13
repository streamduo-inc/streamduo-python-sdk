from auth import *
import requests

def get_table_list():
    table_response = requests.get(f"{ENDPOINT_BASE_URL}/stream/list", headers=get_header())
    print(table_response)
    return table_response.json()

