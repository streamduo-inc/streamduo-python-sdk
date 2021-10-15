
from optparse import OptionParser
from streamduo import auth
from streamduo import organization
from streamduo import stream
parser = OptionParser()
parser.add_option("-p", "--production",
                  action="store_true", dest="production", default=False,
                  help="run against http://api.streamduo.com:8080")
(options, args) = parser.parse_args()

auth_manager = auth.AuthManager()

if options.production:
    auth_manager.ENDPOINT_BASE_URL = "http://api.streamduo.com:8080"
else:
    auth_manager.ENDPOINT_BASE_URL = "http://localhost:8080"




#Delete Stream
print (f"Delete Stream: {stream.delete_stream(auth_manager, new_stream_id)}")



print(f"Delete org result: {organization.delete_organization(auth_manager, new_org_id)}")
print(f"Delete org result: {organization.delete_organization(auth_manager, counter_org_id)}")
print(f"Get Org by ID {organization.get_organization(auth_manager, new_org_id)}")
exit()