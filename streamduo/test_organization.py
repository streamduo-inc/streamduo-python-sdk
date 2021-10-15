from unittest import TestCase
from streamduo import auth
from streamduo import organization

class Test(TestCase):
    def test_get_organization(self):
        auth_manager = auth.AuthManager()
        out = organization.get_organization(auth_manager, "asdf")
        self.fail()
