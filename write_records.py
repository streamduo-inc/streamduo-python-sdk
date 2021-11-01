from streamduo.auth import AuthManager
from streamduo import record



if __name__ == "__main__":
    auth_manager = AuthManager("",
                               "")
    auth_manager.get_header()
    payload = {"name": "Fred",
               "age":27,
               "stats": [{"home runs": 25},
                         {"runs": 43}],
               "position": "pitcher"
               }
    stream = "b29e979f-001d-4633-8d9a-dbb18b44c034"
    record.write_record(auth_manager, stream, payload)

    payload = {"name": "Bob",
               "age":27,
               "stats": [{"home runs": 33},
                         {"runs": 11}],
               "position": "catcher"
               }
    record.write_record(auth_manager, stream, payload)


