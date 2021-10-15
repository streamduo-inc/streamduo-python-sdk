from behave import given, when, then, step
from streamduo import auth
from streamduo import  organization
@given('we are logged in')
def step_impl(context):
    context.auth_manager = auth.AuthManager()
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
    context.org_dict = {}
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
    print(context.org_dict)
    assert user in context.org_dict[org]['users']




