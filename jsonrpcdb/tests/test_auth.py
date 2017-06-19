from unittest import TestCase
from jsonrpcdb.auth import TokenAuth, FN_USERNAME, FN_PASSWORD


class TestAuth(TestCase):
    def test_is_auth(self):
        auth = TokenAuth(None, 'test', 'test')
        self.assertEqual(False, auth.is_auth())
        auth.set_token('test token')
        self.assertEqual(True, auth.is_auth())

    def test_get_auth_dict(self):
        auth_dict = {
            FN_USERNAME: 'user1',
            FN_PASSWORD: 'pass1'
        }
        auth = TokenAuth(None, 'user1', 'pass1')
        self.assertEqual(auth_dict, auth.get_auth_dict())
