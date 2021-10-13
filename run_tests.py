
from optparse import OptionParser
from streamduo import auth
parser = OptionParser()
parser.add_option("-l", "--localhost",
                  action="store_true", dest="local", default=False,
                  help="run against localhost")
(options, args) = parser.parse_args()

if options.local:
    auth_manager = auth.AuthManager()
    print(f"health check: {auth_manager.get_health()}")
    print(f"DB connect check: {auth_manager.get_table_list()}")
else:
    exit()