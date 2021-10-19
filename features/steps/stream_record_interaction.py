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

@when('we query all unread records in stream {stream_name}')
def get_all_unread(context, stream_name):
    print("Read all unread result")
    context.query_result = record.get_all_unread_records(context.auth_manager,
                               context.stream_dict[stream_name]['streamId'])
    print(context.query_result)


@then ('length of resultSet is {result_len}')
def check_length_resultset(context, result_len):
    assert len(context.query_result) == int(result_len)

@then('record {record_name} is in resultSet')
def check_record_in_resultset(context, record_name):
    found = False
    for r in context.query_result:
        if r['recordId'] == context.record_dict[record_name]['recordId']:
            found = True
    assert found == True


@then('record {record_name} is not in resultSet')
def check_record_not_in_resultset(context, record_name):
    found = False
    for r in context.query_result:
        if r['recordId'] == context.record_dict[record_name]['recordId']:
            found = True
    assert found == False
