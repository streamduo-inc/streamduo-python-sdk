import requests
import json


def write_record(auth_manager, stream_id, payload):
    write_stream_record_response = requests.post(f"{auth_manager.ENDPOINT_BASE_URL}/stream/{stream_id}/record/",
                                           headers=auth_manager.header,
                                           json=payload)
    return json.loads(write_stream_record_response.content)