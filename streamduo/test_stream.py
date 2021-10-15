from unittest import TestCase
import stream
import auth


class Test(TestCase):
    auth_manager = auth.AuthManager()
    def test_put_stream(self):
        stream.put_stream(self.auth_manager, "display name", 'prodorgid', 'consorgid')

