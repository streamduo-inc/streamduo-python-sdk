from unittest import TestCase
import os
from streamduo.client import Client


class TestStream(TestCase):


    def test_create_stream(self):
        display_name = 'test_stream'
        stream_controller = Client(os.getenv('AUTH_CLIENT_ID'), os.getenv('AUTH_CLIENT_SECRET')).get_stream_controller()
        stream_request_result = stream_controller.create_stream(display_name)
        assert stream_request_result.json()['displayName'] == display_name
        ## Cleanup
        stream_controller.delete_stream(stream_request_result.json()['streamId'])

    def test_get_stream(self):
        display_name = 'test_stream'
        stream_controller = Client(os.getenv('AUTH_CLIENT_ID'), os.getenv('AUTH_CLIENT_SECRET')).get_stream_controller()
        new_stream_id = stream_controller.create_stream(display_name).json()['streamId']
        stream_request_result = stream_controller.get_stream(new_stream_id)
        assert stream_request_result.json()['streamId'] == new_stream_id
        ## Cleanup
        stream_controller.delete_stream(new_stream_id)

    def test_delete_stream(self):
        display_name = 'test_stream'
        stream_controller = Client(os.getenv('AUTH_CLIENT_ID'), os.getenv('AUTH_CLIENT_SECRET')).get_stream_controller()
        new_stream_id = stream_controller.create_stream(display_name).json()['streamId']
        stream_request_result = stream_controller.get_stream(new_stream_id)
        ## Assert was created
        assert stream_request_result.json()['streamId'] == new_stream_id
        stream_delete_result = stream_controller.delete_stream(new_stream_id)
        assert stream_delete_result.status_code == 204
        ## Assert 404
        stream_request_result_2 = stream_controller.get_stream(new_stream_id)
        assert stream_request_result_2.status_code == 404

    def test_manage_machine_clients(self):
        display_name = 'test_stream'
        stream_controller = Client(os.getenv('AUTH_CLIENT_ID'), os.getenv('AUTH_CLIENT_SECRET')).get_stream_controller()
        new_stream_id = stream_controller.create_stream(display_name).json()['streamId']
        client_display_name = 'test_client'
        add_client_response = stream_controller.add_new_machine_client_to_stream(new_stream_id, client_display_name)
        ##get new client ID
        new_client_id = None
        for i in add_client_response.json()['streamActorPermissionRecords']:
            if i['actorDisplayName'] == client_display_name:
                new_client_id = i['actorId']
                break
        assert new_client_id is not None

        ## Remove Client ID from stream permissions
        remove_client_response = stream_controller.remove_machine_client_from_stream(new_stream_id, new_client_id)
        check_client_id = None
        for i in remove_client_response.json()['streamActorPermissionRecords']:
            if i['actorDisplayName'] == client_display_name:
                check_client_id = i['actorId']
                break
        assert check_client_id is None
        assert len(remove_client_response.json()['streamActorPermissionRecords']) == 1

        ## Cleanup
        actor_controller = Client(os.getenv('AUTH_CLIENT_ID'), os.getenv('AUTH_CLIENT_SECRET')).get_actor_controller()
        actor_controller.delete_machine_client(new_client_id)
        stream_controller.delete_stream(new_stream_id)
        assert actor_controller.get_machine_client(new_client_id).status_code == 404
