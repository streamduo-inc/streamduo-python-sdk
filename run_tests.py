
from optparse import OptionParser
from streamduo import auth
from streamduo import organization
parser = OptionParser()
parser.add_option("-l", "--localhost",
                  action="store_true", dest="local", default=False,
                  help="run against localhost")
(options, args) = parser.parse_args()

if options.local:
    auth_manager = auth.AuthManager()
    print(f"health check: {auth_manager.get_health()}")
    print(f"DB connect check: {auth_manager.get_table_list()}")
    new_org_id = organization.put_new_organization(auth_manager).text
    print(f"Create Organization check: {new_org_id}")
    print(f"Get Org by ID {organization.get_organization(auth_manager, new_org_id)}")
else:
    exit()