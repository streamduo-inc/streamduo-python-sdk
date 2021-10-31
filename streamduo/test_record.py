from unittest import TestCase
from auth import AuthManager
import os
from streamduo import record

class Test(TestCase):
    def test_get_record(self):
        auth_manager = AuthManager(os.getenv("AUTH_CLIENT_ID"), os.getenv("AUTH_CLIENT_SECRET"))
        record.get_record(auth_manager, "65eea856-07a1-4bda-b584-ebe7596baf65", "63c02c08-0110-46e5-bd1d-17fa94cca994")

