import requests
import json
import collections

from .error import DataError, DatabaseError, OperationalError, check_response


class Cursor(object):
    """Represent cursor object."""

    def __init__(self, conn, headers=None, payload_template=None):
        """

        Args:
            conn (Connection): Connection object.
            headers (dict): Headers for request.
            payload_template (dict): Payload template.
        """
        self.description = tuple()
        """tuple: This read-only attribute is a sequence of 7-item sequences.
        Each of these sequences contains information describing one result column.
        """
        self.rowcount = -1
        """int: This read-only attribute specifies the number of rows that the last .execute*()
         produced (for DQL statements like SELECT ) or affected (for DML statements like UPDATE or INSERT )."""
        self.arraysize = 1
        self._data = None
        self.conn = conn
        """Connection: Read-only, reference to connection object."""
        self.auth = conn.auth
        if not headers:
            headers = {'content-type': 'application/json'}
        self.headers = headers
        if not payload_template:
            payload_template = self._get_payload_template()
        self.payload_template = payload_template

    def close(self):
        """Do not support, this method with void functionality."""
        pass

    def execute(self, operation, *args):
        """Execute remote procedure.

        Possible types of result returned by request (s - mean scalar):
            * s
            * [s, s, ..., s]
            * dict
            * [different types]
        Args:
            operation (str): Remote method.
            *args: Used only first argument, it should be dict with 'params' key.
        """
        if len(args) == 0:
            params = {
                'params': None
            }
        else:
            params = args[0]
        payload = self.payload_template.copy()
        payload['method'] = operation
        payload.update(params)
        url = self.conn.get_url()
        response = requests.post(url,
                                 json.dumps(payload),
                                 headers=self.headers,
                                 auth=self.auth)
        try:
            response = response.json()
            if self._is_execute_valid(response):
                self._update_rowcount(response)
                check_response(response)
                self._save_data(response)
        except ValueError as e:
            raise OperationalError()

    def executemany(self, operation, *args):
        pass

    def fetchone(self):
        # TODO move by rows
        """Fetch the next row of a query result set, returning a single sequence,
        or None when no more data is available.
        """
        return self._prepare_one_result()

    def fetchall(self):
        if not isinstance(self._data, collections.Iterable) or isinstance(self._data, str):
            # raise DataError("Result of JSON RPC should be Iterable.")
            return [(self._data,)]
        if self._data:
            data = self._data
        else:
            return []
        probe = data[0]
        if isinstance(probe, collections.Iterable):
            if isinstance(probe, collections.Mapping):
                return data
            else:
                return [tuple(el) for el in data]
        else:
            return [(el,) for el in data]

    def _update_rowcount(self, data):
        pass

    def _is_execute_valid(self, data):
        return True

    def _save_data(self, data):
        self._data = data['result']

    def _get_payload_template(self, params=None):
        if not params:
            params = {}
        payload_template = {
            "method": "",
            "params": params,
            "jsonrpc": "2.0",
            "id": 0,
        }
        return payload_template

    def _prepare_one_result(self):
        """ Prepare result for fetchone method.

        Returns:
            * data = [] -> tuple()
            * data = s -> (s,)
            * data = str -> (str, )
            * data = dict -> dict
            * data = [s, s, ..., s] -> (data[0],)
            * data = [str, ...] -> (data[0],)
            * data = [array, ...] -> tuple(data[0])
            * data = [dict, ...] -> data[0]
        """
        if isinstance(self._data, str):
            return (self._data,)  # data = str -> (str, )
        if isinstance(self._data, collections.Mapping):
            return self._data  # data = dict -> dict
        try:
            one = self._data[0]
        except TypeError:
            return (self._data,)  # data = s -> (s,)
        except IndexError:
            return tuple()  # data = [] -> tuple()
        # multiply results in array
        if isinstance(one, collections.Mapping):
            return one  # data = [dict, ...] -> data[0]
        elif isinstance(one, str):
            return (one,)  # data = [str, ...] -> (data[0],)
        else:
            try:
                probe = one[0]
            except TypeError:
                return tuple([one])  # data = [s, s, ..., s] -> (data[0],)
            except IndexError:
                return tuple()
            return tuple(one)
