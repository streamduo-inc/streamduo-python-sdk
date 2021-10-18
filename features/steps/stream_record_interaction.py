import json
from behave import given, when, then
from streamduo import record
import time

@given('a {payload}')
def given_payload(context, payload):
    context.payload = json.loads(payload)

@when('we write {record_name} with payload {payload} to stream {stream_name}')
def write_record(context, record_name, payload, stream_name):
    stream_id = context.stream_dict[stream_name]['streamId']
    context.record_dict[record_name] =  record.write_record(context.auth_manager, stream_id, json.loads(payload))
    print(context.record_dict)

@then('we query the record {record_name} in stream {stream_name} and readStatus is {expected_read_status}')
def read_single_record(context, record_name, stream_name, expected_read_status):
    result =record.get_record(context.auth_manager,
                              context.stream_dict[stream_name]['streamId'],
                              context.record_dict[record_name]['recordId'])
    print(result)
    print(json.loads(result['dataPayload']))
    print(json.loads(result['dataPayload']) == context.record_dict[record_name]['dataPayload'])
    assert result['readStatus'].lower() == expected_read_status.lower()