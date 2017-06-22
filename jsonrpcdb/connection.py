from .auth import TokenAuth
from .cursor import Cursor

try:
    from urllib.parse import urlunparse
except ImportError:
    from urlparse import urlunparse

HTTP_PORT = 80

# Default connection parameters
DEFAULT_PORT = HTTP_PORT
DEFAULT_HOST = 'localhost'
DEFAULT_SCHEMA = 'http'
DEFAULT_PATH = ''


class Connection(object):
    """Database connection object """

    def __init__(self, **kwargs):
        """Create connection object.

        Args:
            schema (str): http/https
            host (str): Host of json-rpc server
            port (str): Port of json-rpc server.
            database (str): Url path
            auth_type (str): Authentication type
        """
        self._prepare_conn_params(**kwargs)
        self._prepare_auth(**kwargs)

    def cursor(self):
        """Return cursor object."""
        return Cursor(self)

    def commit(self):
        """Do not support transactions, this method with void functionality."""
        pass

    def rollback(self):
        """Do not support transactions, this method with void functionality."""
        pass

    def close(self):
        """Do not support close, this method with void functionality."""
        pass

    def get_url(self):
        """Create url string from connection parameters."""
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

    def _prepare_conn_params(self, **kwargs):
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
        self.conn_params = conn_params

    def _prepare_auth(self, **kwargs):
        """Prepare authentication parameters."""
        auth_type = kwargs.get('auth_type', None)
        auth_params = kwargs.get('auth_params', {})
        if auth_type:
            self.auth = self._create_auth(kwargs['user'], kwargs['password'], **auth_params)
        else:
            self.auth = None
        self.conn_params['auth_type'] = auth_type

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

    def _create_auth(self, username, password, **kwargs):
        """ Create auth instance.

        Args:
            username (str): Username.
            password (str): Password.

        Returns:
            TokenAuth: Auth instance.
        """
        return TokenAuth(self, username, password, **kwargs)
