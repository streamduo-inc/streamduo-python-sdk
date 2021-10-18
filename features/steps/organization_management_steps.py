from behave import given, when, then, step
from streamduo import auth
from streamduo import organization
from streamduo import stream

@given('we are logged in')
def step_impl(context):
    context.auth_manager = auth.AuthManager()
    context.org_dict = {}
    context.stream_dict = {}
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

@when('we create a stream named {stream_name} with Producer {producer} and Consumer {consumer}')
def create_stream(context, stream_name, producer, consumer):
    result = stream.put_stream(context.auth_manager, stream_name, context.org_dict[producer]['organizationId'], context.org_dict[consumer]['organizationId'])
    context.stream_dict[stream_name] = result

@then('stream {stream_name} exists when queried')
def get_stream(context, stream_name):
    result = stream.get_stream(context.auth_manager, context.stream_dict[stream_name]['streamId'])
    assert result['streamId'] == context.stream_dict[stream_name]['streamId']

@when('we {action} clientId {client_id} on stream {stream_name} as {role}')
def update_client_id(context, action, client_id, stream_name, role):
    if action not in ['ADD', 'REMOVE'] or role not in ['PRODUCER', 'CONSUMER']:
        exit()
    result = stream.update_stream_client_id(context.auth_manager, context.stream_dict[stream_name]['streamId'], client_id, role, action)
    print("update_client_id")
    print(result)
    context.stream_dict[stream_name]

@then('clientId {client_id} exists in stream {stream_name} as {role}')
def check_client_id(context, client_id, stream_name, role):
    result = stream.get_stream(context.auth_manager, context.stream_dict[stream_name]['streamId'])
    print("check_client_id")
    print(result)
    if role == 'PRODUCER':
        assert client_id in result['producerClientIds']
    elif role == 'CONSUMER':
        assert client_id in result['consumerClientIds']

@then('clientId {client_id} does not exist in stream {stream_name} as {role}')
def check_client_id_ne(context, client_id, stream_name, role):
    result = stream.get_stream(context.auth_manager, context.stream_dict[stream_name]['streamId'])
    if role == 'PRODUCER':
        assert client_id not in result['producerClientIds']
    elif role == 'CONSUMER':
        assert client_id not in result['consumerClientIds']

@when('we delete stream {stream_name}')
def delete_stream(context, stream_name):
    result = stream.delete_stream(context.auth_manager, context.stream_dict[stream_name]['streamId'])

@then('the stream {stream_name} does not exist when queried')
def confirm_stream_delete(context, stream_name):
    result = stream.get_stream(context.auth_manager, context.stream_dict[stream_name]['streamId'])
    assert result is None