from unittest import TestCase
import jsonrpcdb as Database
from jsonrpcdb.auth import TokenAuth
from jsonrpcdb.error import ProgrammingError


class ConnectionTest(TestCase):
    def test_empty_conn_params(self):
        conn_params = {}
        conn = Database.connect(**conn_params)
        self.assertEqual('http://localhost', conn.get_url())

    def test_conn_params(self):
        conn_params = {
            'database': 'json-rpc.php'
        }
        conn = Database.connect(**conn_params)
        self.assertEqual('http://localhost/json-rpc.php', conn.get_url())

        conn_params = {
            'database': '/json-rpc.php'
        }
        conn = Database.connect(**conn_params)
        self.assertEqual('http://localhost/json-rpc.php', conn.get_url())

        conn_params = {
            'host': 'test.com',
            'port': 4000,
            'database': '/json-rpc.php'
        }
        conn = Database.connect(**conn_params)
        self.assertEqual('http://test.com:4000/json-rpc.php', conn.get_url())

        conn_params = {
            'schema': 'https',
            'host': 'test.com',
            'port': 4000,
            'database': '/json-rpc.php'
        }
        conn = Database.connect(**conn_params)
        self.assertEqual('https://test.com:4000/json-rpc.php', conn.get_url())

    def test_is_protect(self):
        conn_params = {
            'port': 4000,
            'user': 'test',
            'password': 'test',
            'auth_type': 'token'
        }
        conn = Database.connect(**conn_params)
        self.assertEqual(True, conn.is_protected())

    def test_is_auth(self):
        conn_params = {
            'port': 4000,
            'user': 'test',
            'password': 'test',
            'auth_type': 'token'
        }
        conn = Database.connect(**conn_params)
        self.assertEqual(True, conn.is_auth())

    def test_protected_res(self):
        conn_params = {
            'port': 4000,
            'user': 'test',
            'password': 'test',
            'auth_type': 'token'
        }
        conn = Database.connect(**conn_params)
        cur = conn.cursor()
        data = {
            'params': [1]
        }
        cur.execute('protected_res', data)
        result = cur.fetchone()
        self.assertEqual((1,), result)
        cur.auth.set_token('fail_token')
        with self.assertRaises(ProgrammingError):
            cur.execute('protected_res', data)
