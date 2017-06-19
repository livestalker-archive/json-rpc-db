import requests
import json
import collections
from .auth import TokenAuth
from .error import DataError

ONE = 0
MULTI = 1


class Cursor(object):
    def __init__(self, conn, headers=None, payload_template=None):
        self.rowcount = -1
        self.arraysize = 1
        self._data = []
        self.conn = conn
        self.auth = conn.auth
        if not headers:
            headers = {'content-type': 'application/json'}
        self.headers = headers
        if not payload_template:
            payload_template = self._get_payload_template()
        self.payload_template = payload_template

    def close(self):
        pass

    def execute(self, operation, *args):
        payload = self.payload_template.copy()
        payload['method'] = operation
        # TODO IndexError
        payload.update(args[0])
        url = self.conn.get_url()
        # TODO JSONDecodeError
        response = requests.post(url,
                                 json.dumps(payload),
                                 headers=self.headers,
                                 auth=self.auth)
        response = response.json()
        if self._is_execute_valid(response):
            self._update_rowcount(response)
            self._save_data(response)
            # TODO raise

    def executemany(self, operation, *args):
        pass

    def fetchone(self):
        if not isinstance(self._data, collections.Iterable) or isinstance(self._data, str):
            # raise DataError("Result of JSON RPC should be Iterable.")
            return (self._data,)
        if self._data:
            one = self._data[0]
        else:
            return tuple()
        if isinstance(one, collections.Iterable):
            if isinstance(one, collections.Mapping):
                return one
            else:
                return tuple(one)
        else:
            return tuple([one])

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
