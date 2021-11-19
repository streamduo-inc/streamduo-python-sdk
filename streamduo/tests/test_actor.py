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

    def test_list_machine_client(self):

        actor_controller = Client(os.getenv('AUTH_CLIENT_ID'), os.getenv('AUTH_CLIENT_SECRET')).get_actor_controller()
        #clear out list
        client_list = actor_controller.get_clients()
        for client in client_list.json():
            print(client['clientId'])
            actor_controller.delete_machine_client(client['clientId'])
        client_list_new = actor_controller.get_clients()
        assert len(client_list_new.json()) == 0

        #create new client
        create_actor_response = actor_controller.create_machine_client("client display name test",
                                                                      "client description test")
        new_client_id = create_actor_response.json()['clientId']

        #get client list
        client_list = actor_controller.get_clients()

        new_client_found = False
        for client in client_list.json():
            if client['clientId'] == new_client_id:
                new_client_found = True
                break
        assert new_client_found == True

        ##cleanup
        actor_controller.delete_machine_client(new_client_id)

        client_list_new = actor_controller.get_clients()
        assert len(client_list_new.json()) == 0


    def test_too_many_machine_client(self):
        actor_controller = Client(os.getenv('AUTH_CLIENT_ID'), os.getenv('AUTH_CLIENT_SECRET')).get_actor_controller()

        #clear out list
        client_list = actor_controller.get_clients()
        for client in client_list.json():
            print(client['clientId'])
            actor_controller.delete_machine_client(client['clientId'])
        client_list_new = actor_controller.get_clients()
        assert len(client_list_new.json()) == 0

        create_actor_response = actor_controller.create_machine_client("client display name test",
                                                                       "client description test")
        create_actor_response2 = actor_controller.create_machine_client("client display name test2",
                                                                       "client description test2")
        create_actor_response3 = actor_controller.create_machine_client("client display name test3",
                                                                       "client description test3")
        create_actor_response4 = actor_controller.create_machine_client("client display name test4",
                                                                       "client description test4")
        assert create_actor_response4.json()['message']  == "Max Number of Clients Exceeded"

        #clear out list
        client_list = actor_controller.get_clients()
        for client in client_list.json():
            print(client['clientId'])
            actor_controller.delete_machine_client(client['clientId'])
        client_list_new = actor_controller.get_clients()
        assert len(client_list_new.json()) == 0


