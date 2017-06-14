from unittest import TestCase
import jsonrpcdb as Database


class ConnectionTest(TestCase):
    def setUp(self):
        conn_param = {
            'host': 'localhost',
            'port': 4000,
            'database': 'jsonrpc',
            'user': '',
            'password': ''
        }
        self.conn = Database.connect(**conn_param)

    def test_get_url(self):
        dsn = 'http://localhost:4000/jsonrpc'
        self.assertEqual(dsn, self.conn.get_url())
        self.conn.conn_params['schema'] = 'https'
        dsn = 'https://localhost:4000/jsonrpc'
        self.assertEqual(dsn, self.conn.get_url())
        dsn = 'https://localhost:4000/'
        del self.conn.conn_params['database']
        self.assertEqual(dsn, self.conn.get_url())
        del self.conn.conn_params['port']
        self.conn.conn_params['schema'] = 'http'
        dsn = 'http://localhost/'
        self.assertEqual(dsn, self.conn.get_url())
