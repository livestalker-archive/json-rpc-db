from .connection import Connection

__version = (0, 1, 0)
__version__ = version = '.'.join(map(str, __version))
__project__ = PROJECT = __name__

apilevel = '2.0'
threadsafety = 3
paramstyle = 'pyformat'

from .error import Error, InterfaceError, DatabaseError, DataError, OperationalError, IntegrityError, InternalError, \
    ProgrammingError, NotSupportedError


def connect(*args, **kwargs):
    """Create new connection to database.

    scheme://host[:port]][/path]

    Args:
        *args: positional arguments (not using at the moment)

    Kwargs:
        user (str): username
        password (str): password
        host (str): json-rpc host
        port (int): port
        database (str): path
        schema (str): http/https
        auth_type (str): authentication type (token)

    Returns:
        Connection: connection object
    """
    return Connection(**kwargs)
