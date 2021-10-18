import json
from behave import given, when, then
from streamduo import record
import time

@given('a {payload}')
def given_payload(context, payload):
    context.payload = json.loads(payload)

@when('we write {payload} to stream {stream_name}')
def write_record(context, payload, stream_name):
    time.sleep(30)
    stream_id = context.stream_dict[stream_name]['streamId']
    record.write_record(context.auth_manager, stream_id, json.loads(payload))
