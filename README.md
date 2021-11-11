# streamduo-python-sdk




sdk for easy interaction with [StreamDuo](https://streamduo.com) APIs

_Easily write records..._

```python
from streamduo.client import Client

record_controller = Client(os.getenv('AUTH_CLIENT_ID'), os.getenv('AUTH_CLIENT_SECRET')).get_record_controller()

payload = {
            'Part Description': 'Widget A',
            'Price': 10.00,
            'Inventory': 20000
        }

write_response = record_controller.write_record(stream_id, payload)

# write_response is the `Record` object of our newly written record...
record_id = write_response.json()['recordId']

```

_and read records..._

```python
from streamduo.client import Client

record_controller = Client(os.getenv('AUTH_CLIENT_ID'), os.getenv('AUTH_CLIENT_SECRET')).get_record_controller()

# read the next 5 unread records
read_unread_response = record_controller.read_unread_records(stream_id, True, 5)

for record in read_unread_response.json():
  print(record['recordId'])

```


See the [Docs](https://docs.streamduo.com/docs/python-sdk-installation) for full details on using the SDK.



