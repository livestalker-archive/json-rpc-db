from unittest import TestCase
from jsonrpcdb.error import DataError
import jsonrpcdb as Database


class CursorTest(TestCase):
    def setUp(self):
        conn_param = {
            'database': '',
            'user': '',
            'password': '',
            'schema': 'http',
            'host': 'localhost',
            'port': 4000
        }
        self.conn = Database.connect(**conn_param)

    def test_scalar_fetchone(self):
        """
        Execute function scalar.

        Result of function - scalar.
        Result of fetch - DataError.
        """
        data = {
            'params': [1]
        }
        cur = self.conn.cursor()
        cur.execute('scalar', data)
        result = cur.fetchone()
        self.assertEqual((1,), result)

    def test_list_of_scalar_fetchone(self):
        """
        Execute function add.

        Result of function - list of scalars.
        Result of fetch - tuple.
        """
        data = {
            'params': [2]
        }
        cur = self.conn.cursor()
        cur.execute('list_of_scalar', data)
        result = cur.fetchone()
        self.assertEqual((2,), result)

    def test_list_of_list_fetchone(self):
        """
        Execute function list_of_list.

        Result of function - list of list.
        Result of fetch - tuple.
        """
        data = {
            'params': [3]
        }
        cur = self.conn.cursor()
        cur.execute('list_of_list', data)
        result = cur.fetchone()
        self.assertEqual((3, 3, 3), result)

    def test_list_of_dict_fetchone(self):
        """
        Check simple function list_of_dict.

        Result of function - list of dict.
        Result of fetch - dict.
        """
        arr = [4]
        data = {
            'params': arr
        }
        cur = self.conn.cursor()
        cur.execute('list_of_dict', data)
        result = cur.fetchone()
        self.assertEqual({'a': 4}, result)

    def test_prepare_one_result(self):
        cur = self.conn.cursor()
        data = [
            [],
            1,
            'test',
            {'1': 1, '2': 2},
            [1, 2, 3, 4],
            ['test1', 'test2'],
            [[1, 2, 3]],
            [{'1': 1, '2': 2}],
            [[]]
        ]
        must_be = [
            tuple(),
            (1, ),
            ('test', ),
            {'1': 1, '2': 2},
            (1, ),
            ('test1', ),
            (1, 2, 3),
            {'1': 1, '2': 2},
            tuple()
        ]
        for ix in range(len(data)):
            cur._data = data[ix]
            res = cur._prepare_one_result()
            self.assertEqual(must_be[ix], res)
