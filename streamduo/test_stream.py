from unittest import TestCase

import streamduo.stream


class Test(TestCase):
    def test_get_oauth_token(self):
        token_response = streamduo.stream.get_oauth_token()
        print(token_response)