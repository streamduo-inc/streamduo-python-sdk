# streamduo-python-sdk


This SDK is developed for ease of use with the [StreamDuo](https://streamduo.com) APIs.

StreamDuo is a platform for data transfers, optimized for the structured data that Data Engineers use most. 

For details on the API interface, see the [Swagger Docs](https://api.streamduo.com/swagger-ui/index.html?configUrl=/v3/api-docs/swagger-config).


## Examples of the SDK in action

_Create a data stream..._

```python
from streamduo import Client
client = Client(os.getenv('AUTH_CLIENT_ID'), os.getenv('AUTH_CLIENT_SECRET'))

stream_controller = client.get_stream_controller()

stream_request_result = stream_controller.create_stream('my new stream')

stream_id = stream_request_result.json()['streamId']

```

_add a data schema and set active..._

```python


schema_controller = client.get_schema_controller()
with open("car_schema.json", 'r') as file:
            car_schema = json.load(file)
create_schema_response = schema_controller.create_schema(stream_id=stream_id,
                                                      schema=car_schema, 
                                                      schema_type=SchemaType.JSON)
schema_id = create_schema_response.json()['schemaId']


## Set new Schema active
set_active_response = schema_controller.set_active_schema(stream_id=stream_id, schema_id=schema_id)

```

_generate an encryption key and set it as active..._
```python
key_controller = client.get_key_controller()

key_request = {'publicKeyAlgorithm': KeyAlgorithm.CURVE25519.value,
           'publicKeyEncoding': KeyEncoding.BASE64.value,
           'publicKeyDescription': "test key integration"}
new_key_resp = key_controller.create_key_server(new_stream_id, key_request)

key_id = new_key_resp.json()['publicKey']['publicKeyId']
private_key = new_key_resp.json()['privateKeyValue']
public_key = new_key_resp.json()['publicKey']['publicKeyValue']


## Set new key active
set_key_active_response = key_controller.set_active_key(stream_id=stream_id, key_id=key_id)
```


_upload a file, validated and encrypted..._
```python
batch_controller = client.get_batch_controller()

batch_data = batch_controller.send_file(stream_id=stream_id, file_path="data.csv")
batch_id = batch_data.batchId
```



_download a file, validated and decrypted..._
```python
batch_metadata = batch_controller.get_batch(stream_id=stream_id,
                       batch_id=batch_id,
                       destination_filepath="downloaded.csv",
                       decryption_key=private_key)
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





