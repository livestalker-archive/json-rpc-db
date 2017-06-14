from .connection import Connection

apilevel = '2.0'
threadsafety = 3
paramstyle = 'pyformat'

from .error import Error, InterfaceError, DatabaseError, DataError, OperationalError, IntegrityError, InternalError, \
    ProgrammingError, NotSupportedError


def connect(**kwargs):
    """
    Create new database connection.

    The basic connection parameters are:
    scheme:[//[user[:password]@]host[:port]][/path][?query][#fragment]

    - *database*: path
    - *user*: user name used to authenticate
    - *password*: password used to authenticate
    - *host*: json-rpc host
    - *port*: connection port number
    - *scheme*: http/https
    - *auth_type*: None - without authentication, 'token' - token authorization
    - *auth_field*: Field name for payload in token authorization
    - *auth_method*: authentication JSON-RPC method
    """
    return Connection(**kwargs)
