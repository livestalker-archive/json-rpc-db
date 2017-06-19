from requests import auth
import json
import requests

FN_USERNAME = 'user'
"""str: Default field name for username.

Using in params options of json-rpc payload.
"""
FN_PASSWORD = 'password'
"""str: Default field name for password.

Using in params options of json-rpc payload.
"""
FN_AUTH = 'auth'
"""str: Default field name for authentication.

Using in payload of json-rpc.
"""
DEFAULT_AUTH_METHOD = 'login'
"""Default login method."""


class TokenAuth(auth.AuthBase):
    """Auth class for token authentication """

    def __init__(self, conn, username, password,
                 login_method=DEFAULT_AUTH_METHOD,
                 fn_auth=FN_AUTH,
                 fn_username=FN_USERNAME,
                 fn_password=FN_PASSWORD):
        """
    Create AuthToken instance.
        Args:
            conn (Connection): Reference to connection object.
            username (str): Username.
            password (str): Password.
            login_method (str): Login method.
            fn_auth (str): Auth field name for payload.
            fn_username (str): Name of username field for params dict in payload.
            fn_password: Name of password field for params dict in payload.
        """
        self.conn = conn
        self.username = username
        self.password = password
        self.login_method = login_method
        self.fn_auth = fn_auth
        self.fn_username = fn_username
        self.fn_password = fn_password
        self.token = None
        if conn:
            self._login()

    def __call__(self, r):
        """Change body of request.

        Add auth field with auth token.

        Args:
            r (PreparedRequest): Prepared request.

        Returns:
            PreparedRequest: Modified request.
        """
        if not self.is_auth():
            self._login()
        json_body = json.loads(r.body)
        json_body[self.fn_auth] = self.token
        r.body = json.dumps(json_body)
        return r

    def is_auth(self):
        return True if self.token else False

    def get_auth_dict(self):
        return {
            self.fn_username: self.username,
            self.fn_password: self.password
        }

    def set_token(self, token):
        """Set auth token.

        Args:
            token (str): Token.
        """
        self.token = token

    def _login(self):
        """Try login and get auth token."""
        payload = {
            "method": self.login_method,
            "params": self.get_auth_dict(),
            "jsonrpc": "2.0",
            "id": 0,
        }
        headers = {'content-type': 'application/json'}
        response = requests.post(self.conn.get_url(),
                                 json.dumps(payload),
                                 headers=headers)
        response = response.json()
        # TODO error handler
        self.set_token(response['result'])
