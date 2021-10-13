from unittest import TestCase
import auth

class Test(TestCase):
    def test_get_health(self):
        auth.get_health()

class Test(TestCase):
    def test_get_oauth_token(self):
        token_response = auth.get_oauth_token()
        print(token_response)
