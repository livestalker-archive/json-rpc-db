try:
    from exceptions import Exception, StandardError, Warning
except ImportError:
    # Python 3
    StandardError = Exception

# Standart json-rpc error codes
PARSE_ERROR = -32700
INVALID_REQUEST = -32600
METHOD_NOT_FOUND = -32601
INVALID_PARAMS = -32602
INTERNAL_ERROR = -32603


class Warning(Warning):
    """Exception raised for important warnings like data truncations
       while inserting, etc."""


class Error(Exception):
    """Exception that is the base class of all other error exceptions
        (not Warning)."""


class InterfaceError(Error):
    """Exception raised for errors that are related to the database
        interface rather than the database itself."""


class DatabaseError(Error):
    """Exception raised for errors that are related to the
       database."""


class DataError(DatabaseError):
    """Exception raised for errors that are due to problems with the
       processed data like division by zero, numeric value out of range,
       etc."""


class OperationalError(DatabaseError):
    """Exception raised for errors that are related to the database's
       operation and not necessarily under the control of the programmer,
       e.g. an unexpected disconnect occurs, the data source name is not
       found, a transaction could not be processed, a memory allocation
       error occurred during processing, etc."""


class IntegrityError(DatabaseError):
    """Exception raised when the relational integrity of the database
       is affected, e.g. a foreign key check fails, duplicate key,
       etc."""


class InternalError(DatabaseError):
    """Exception raised when the database encounters an internal
       error, e.g. the cursor is not valid anymore, the transaction is
       out of sync, etc."""


class ProgrammingError(DatabaseError):
    """Exception raised for programming errors, e.g. table not found
        or already exists, syntax error in the SQL statement, wrong number
        of parameters specified, etc."""


class NotSupportedError(DatabaseError):
    """Exception raised in case a method or database API was used
        which is not supported by the database, e.g. requesting a
        .rollback() on a connection that does not support transaction or
        has transactions turned off."""


def check_response(response):
    if 'error' not in response:
        return
    error = response['error']
    code = error.get('code', None)
    message = error.get('message', '')
    data = error.get('data', '')
    if code == PARSE_ERROR or code == INVALID_REQUEST:
        raise InterfaceError(code, message, data)
    elif code == METHOD_NOT_FOUND or code == INVALID_PARAMS:
        raise ProgrammingError(code, message, data)
    elif code == INTERNAL_ERROR:
        raise InternalError(code, message, data)
    else:
        raise DatabaseError(code, message, data)
