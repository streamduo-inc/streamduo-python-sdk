
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

#Create counterparty ORG
counter_org_id = organization.put_new_organization(auth_manager)
#Create Stream
new_stream_id = stream.put_stream(auth_manager, 'dtps.io to counter.io', new_org_id, counter_org_id)
print(f"created stream {new_stream_id}")
#get Stream
print(f"Get Stream by ID {stream.get_stream(auth_manager, new_stream_id)}")

print(f"ADD Cient ID as Consumer {stream.update_stream_client_id(auth_manager, new_stream_id, 'clientID1_consumer', 'CONSUMER', 'ADD')}")
print(f"Get Stream by ID V2 {stream.get_stream(auth_manager, new_stream_id)}")
print(f"REMOVE Client ID as Consumer {stream.update_stream_client_id(auth_manager, new_stream_id, 'clientID1_consumer', 'CONSUMER', 'REMOVE')}")

#Delete Stream
print (f"Delete Stream: {stream.delete_stream(auth_manager, new_stream_id)}")



print(f"Delete org result: {organization.delete_organization(auth_manager, new_org_id)}")
print(f"Delete org result: {organization.delete_organization(auth_manager, counter_org_id)}")
print(f"Get Org by ID {organization.get_organization(auth_manager, new_org_id)}")
exit()