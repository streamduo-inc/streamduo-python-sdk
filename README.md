# streamduo-python-sdk


This SDK is developed for ease of use with the [StreamDuo](https://streamduo.com) APIs.

For details on the API interface, see the [Swagger Docs](https://api.streamduo.com/swagger-ui/index.html?configUrl=/v3/api-docs/swagger-config).


## Examples of the SDK in action

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

_upload a schema and set it as active..._
```python
## Add schema to stream
schema_controller = Client(os.getenv('AUTH_CLIENT_ID'), os.getenv('AUTH_CLIENT_SECRET')).get_schema_controller()
with open("car_schema.json", 'r') as file:
    car_schema = json.load(file)

create_schema_response = schema_controller.create_schema(stream_id=stream_id,
                                                      schema=car_schema, schema_type=SchemaType.JSON)
new_schema_id = create_schema_response.json()['schemaId']

## Set new Schema active
set_active_response = schema_controller.set_active_schema(stream_id=stream_id, schema_id=new_schema_id)
```


See the [Docs](https://docs.streamduo.com/docs/python-sdk-installation) for full details on using the SDK.

## Installation

`pip install streamduo`


# Contributing

## Testing

There are two types of tests:

### 1. Unit tests

`streamduo/tests/unit/*`

Requires no authentication, uses a mocked `requests` library.

### 2. Integration tests

`streamduo/tests/integration/*`

Requires client credentials stored as environment variables:

'AUTH_CLIENT_ID'  
'AUTH_CLIENT_SECRET'

Optionally, when running against a development server, the API endpoint can be overridden by the presense of the environment variable:

'STREAMDUO_SDK_URL'





