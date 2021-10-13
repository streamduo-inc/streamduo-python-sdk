from unittest import TestCase
import stream
import auth

class Test(TestCase):
    def test_get_table_list(self):
        auth_manager = auth.AuthManager()
        res= stream.get_table_list(auth_manager)
        print(res)
