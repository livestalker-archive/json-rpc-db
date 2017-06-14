from .cursor import Cursor


class Connection(object):
    def __init__(self, **kwargs):
        self.conn_params = kwargs
        self._check_conn_params()
        if self.is_protected() and not self.is_auth():
            self.conn_params['auth_token'] = self._get_auth_token()

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
        pass

    def get_url(self):
        self._check_conn_params()
        if 'port' not in self.conn_params:
            pattern = '{schema}://{host}/{database}'
        else:
            pattern = '{schema}://{host}:{port}/{database}'
        return pattern.format(**self.conn_params)

    def _check_conn_params(self):
        conn_param = self.conn_params
        if 'schema' not in conn_param:
            conn_param['schema'] = 'http'
        if 'database' not in conn_param:
            conn_param['database'] = ''

    def _get_auth_token(self):
        conn_params = self.conn_params
        cur = self.cursor()
        params = {
            'params': {
                'user': conn_params['user'],
                'password': conn_params['password']
            }
        }
        cur.execute(conn_params['auth_method'], params)
        result = cur.fetchone()
        # TODO IndexError
        return result[0]

    def is_protected(self):
        return True if self.conn_params.get('auth_type', None) else False

    def is_auth(self):
        return True if self.conn_params.get('auth_token', None) else False
