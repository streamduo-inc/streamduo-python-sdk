from behave import given, when, then, step
from streamduo import auth
from streamduo import organization
from streamduo import stream
from streamduo import client
import os

@given('we are logged in')
def step_impl(context):
    context.auth_manager = auth.AuthManager(os.getenv("AUTH_CLIENT_ID"), os.getenv("AUTH_CLIENT_SECRET"))
    context.org_dict = {}
    context.stream_dict = {}
    context.record_dict = {}
    context.client_dict = {}
    #context.auth_manager.ENDPOINT_BASE_URL = "http://api.streamduo.com:8080"
    assert context.auth_manager is not None


@when('we check health')
def check_health(context):
    context.health_status = context.auth_manager.get_health()

@then('health is ok')
def step_impl(context):
    assert context.health_status == "OK"

@when('we create an organization {org} with user {user}')
def create_organization(context, org, user):
    context.org_dict[org] = organization.put_new_organization(context.auth_manager, org, user)

@then('the new org {org} exists when queried')
def query_new_org(context, org):
    result = organization.get_organization(context.auth_manager, context.org_dict[org]['organizationId'])
    assert result['organizationId'] == context.org_dict[org]['organizationId']

@when('we add a user {user} to organization {org}')
def add_user(context, user, org):
    result = organization.add_user(context.auth_manager, context.org_dict[org]['organizationId'], user)
    context.org_dict[org] = result

@then('user {user} has been added to organization {org}')
def check_user(context, user, org):
    assert user in context.org_dict[org]['users']

@when('we delete organization {org}')
def delete_org(context, org):
    result = organization.delete_organization(context.auth_manager, context.org_dict[org]['organizationId'])

@then('the organization {org} does not exist when queried')
def confirm_delete(context, org):
    result = organization.get_organization(context.auth_manager, context.org_dict[org]['organizationId'])
    assert result is None

@when('we create a stream named {stream_name}')
def create_stream(context, stream_name):
    result = stream.put_stream(context.auth_manager, stream_name)
    context.stream_dict[stream_name] = result

@then('stream {stream_name} exists when queried')
def get_stream(context, stream_name):
    print(context.stream_dict)
    result = stream.get_stream(context.auth_manager, context.stream_dict[stream_name]['streamId'])
    assert result['streamId'] == context.stream_dict[stream_name]['streamId']

@then('clientId {client_id} exists in stream {stream_name} as {role}')
def check_client_id(context, client_id, stream_name, role):
    result = stream.get_stream(context.auth_manager, context.stream_dict[stream_name]['streamId'])
    print("check_client_id")
    print(result)
    found = False
    for permission in result['streamActorPermissionRecords']:
        if permission['actorDisplayName'] == client_id:
            if permission['isProducer'] and role == 'PRODUCER':
                found = True
            if permission['isConsumer'] and role == 'CONSUMER':
                found = True
    assert found == True

@then('clientId {client_id} does not exist in stream {stream_name} as {role}')
def check_client_id_ne(context, client_id, stream_name, role):
    result = stream.get_stream(context.auth_manager, context.stream_dict[stream_name]['streamId'])
    found = False
    for permission in result['streamActorPermissionRecords']:
        if permission['actorDisplayName'] == client_id and permission['actorRole'] == role:
            found = True
    assert found == False

@when('we delete stream {stream_name}')
def delete_stream(context, stream_name):
    result = stream.delete_stream(context.auth_manager, context.stream_dict[stream_name]['streamId'])

@then('the stream {stream_name} does not exist when queried')
def confirm_stream_delete(context, stream_name):
    result = stream.get_stream(context.auth_manager, context.stream_dict[stream_name]['streamId'])
    assert result is None

@when('we create a new clientId named {client_name} on our stream {stream_name} as {role}')
def create_new_client_id(context, client_name, stream_name, role):
    if role not in ['PRODUCER', 'CONSUMER']:
        exit()
    result = stream.add_new_client_id(context.auth_manager, client_name, context.stream_dict[stream_name]['streamId'], role)
    for permission in result['streamActorPermissionRecords']:
        if permission['actorDisplayName'] == client_name:
            context.client_dict[client_name] = {}
            context.client_dict[client_name]['client_id'] = permission['actorId']


@then('we delete clientId named {client_name}')
def delete_client(context, client_name):
    client.delete_client(context.auth_manager, context.client_dict[client_name]['client_id'])