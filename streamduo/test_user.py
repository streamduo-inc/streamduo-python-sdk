from unittest import TestCase
from auth import AuthManager
from user import *

class Test(TestCase):

    def test_create_user(self):
        auth_manager = AuthManager()
        create_user(auth_manager)

    def test_get_user(self):
        auth_manager = AuthManager()
        print(get_user(auth_manager))

    def test_get_health(self):
        auth_manager = AuthManager()
        get_health(auth_manager)

