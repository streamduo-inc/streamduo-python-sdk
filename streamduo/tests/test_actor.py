import os
from unittest import TestCase

from streamduo.client import Client


class TestActor(TestCase):
    def test_create_machine_client(self):
        actor_controller = Client(os.getenv('AUTH_CLIENT_ID'), os.getenv('AUTH_CLIENT_SECRET')).get_actor_controller()
        create_actor_response = actor_controller.create_machine_client("client display name test",
                                                                       "client description test")
        new_client_id = create_actor_response.json()['clientId']
        assert new_client_id is not None

        ## cleanup
        delete_response = actor_controller.delete_machine_client(new_client_id)
        assert delete_response.status_code == 204

        ## check get
        get_response = actor_controller.get_machine_client(new_client_id)
        assert get_response.status_code == 404
