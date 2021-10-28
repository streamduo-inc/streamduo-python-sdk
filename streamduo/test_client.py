from unittest import TestCase
from auth import AuthManager, MgmtAuthManager
from client import *

class Test(TestCase):
    def test_cleanup_clients(self):
        auth_manager = MgmtAuthManager()
        cleanup_clients(auth_manager)
