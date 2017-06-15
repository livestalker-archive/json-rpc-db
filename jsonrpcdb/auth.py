from requests import auth


class TokenAuth(auth.AuthBase):
    def __call__(self, r):
        pass
