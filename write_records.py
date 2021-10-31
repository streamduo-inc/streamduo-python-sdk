from streamduo.auth import AuthManager
from streamduo import record



if __name__ == "__main__":
    auth_manager = AuthManager("v3QzBbTSU3nJSXD3bRZxrMRlsR7cFQX7",
                               "RTYCJcTHY-grd0sxKA1qxlcUWo-TxJfiORk6NKOg9vvU-ZR5HL_zOAU-sSy4YTTL")
    payload = {"name": "Fred",
               "age":27,
               "stats": [{"home runs": 25},
                         {"runs": 43}],
               "position": "pitcher"
               }
    stream = "f07e9891-645c-4a16-a99d-fead759107fb"
    record.write_record(auth_manager, stream, payload)

