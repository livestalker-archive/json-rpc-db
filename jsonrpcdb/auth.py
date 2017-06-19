from requests import auth
import json
import requests

FN_USERNAME = 'user'
FN_PASSWORD = 'password'
FN_AUTH = 'auth'
DEFAULT_AUTH_METHOD = 'login'


class TokenAuth(auth.AuthBase):
    def __init__(self, conn, username, password,
                 login_method=DEFAULT_AUTH_METHOD,
                 fn_auth=FN_AUTH,
                 fn_username=FN_USERNAME,
                 fn_password=FN_PASSWORD):
        self.conn = conn
        self.username = username
        self.password = password
        self.login_method = login_method
        self.fn_auth = fn_auth
        self.fn_username = fn_username
        self.fn_password = fn_password
        self.token = None
        self._login()

    def __call__(self, r):
        json_body = json.loads(r.body)
        if not self.is_auth():
            pass
        else:
            pass

    def is_auth(self):
        return True if self.token else False

    def get_auth_dict(self):
        return {
            self.fn_username: self.username,
            self.fn_password: self.password
        }

    def set_token(self, token):
        self.token = token

    def _login(self):
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
