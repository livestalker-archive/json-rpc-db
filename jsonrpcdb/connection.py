from .auth import TokenAuth
from .cursor import Cursor

try:
    from urllib.parse import urlunparse
except ImportError:
    from urlparse import urlunparse

HTTP_PORT = 80
DEFAULT_PORT = HTTP_PORT
DEFAULT_HOST = 'localhost'
DEFAULT_SCHEMA = 'http'
DEFAULT_PATH = ''

AUTH_TOKEN = 'token'


class Connection(object):
    """Database connection object """

    def __init__(self, **kwargs):
        """Create connection object.

        Args:
            **kwargs: connection parameters
        """
        self.conn_params = self._check_conn_params(**kwargs)
        self._check_auth_params(**kwargs)

    def cursor(self):
        return Cursor(self)

    def commit(self):
        """
        Do not support transactions, this method with void functionality.
        """
        pass

    def rollback(self):
        """
        Do not support transactions, this method with void functionality.
        """
        pass

    def close(self):
        """
        Do not support close, this method with void functionality.
        """
        pass

    def get_url(self):
        """Create url string from connection parameters.

        """
        conn_params = self.conn_params
        if conn_params['port'] != HTTP_PORT:
            host = '{}:{}'.format(conn_params['host'], conn_params['port'])
        else:
            host = conn_params['host']
        url_parts = (
            conn_params['schema'],
            host,
            conn_params['database'],
            '',
            '',
            '',
        )
        return urlunparse(url_parts)

    def _check_conn_params(self, **kwargs):
        """Check connection parameters.

        Fill empty parameters with default values.

        Args:
            **kwargs: connection parameters

        Returns:
            dict: Return filled dictionary with connection parameters.

        """
        conn_params = {}
        conn_params['database'] = kwargs.get('database', DEFAULT_PATH)
        conn_params['host'] = kwargs.get('host', DEFAULT_HOST)
        conn_params['port'] = kwargs.get('port', DEFAULT_PORT)
        conn_params['schema'] = kwargs.get('schema', DEFAULT_SCHEMA)
        return conn_params

    def _check_auth_params(self, **kwargs):
        auth_type = kwargs.get('auth_type', None)
        if auth_type:
            self.auth = self._create_auth(kwargs['user'], kwargs['password'])
        else:
            self.auth = None
        self.conn_params['auth_type'] = auth_type

    def _get_auth_token(self):
        conn_params = self.conn_params
        cur = self.cursor()
        params = {
            'params': {
                'user': conn_params['user'],
                'password': conn_params['password']
            }
        }
        cur.execute(conn_params['auth']['method'], params)
        result = cur.fetchone()
        # TODO IndexError
        return result[0]

    def is_protected(self):
        """Is json rpc protected?

        Returns:
          bool: Return True if auth key present in connection parameters.
        """
        return True if self.conn_params.get('auth_type', None) else False

    def is_auth(self):
        """Are we authorized?

        Returns:
            bool: Return True if we have auth-token.
        """
        auth = self.auth
        if auth:
            auth_token = auth.token
            return True if auth_token else False
        return False

    def _create_auth(self, username, password):
        return TokenAuth(self, username, password)
