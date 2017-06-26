JSON-RPC DB
===========

|Build Status| |Codacy Badge| |Codacy Badge|

Primary goal
------------

This library realize Python Database API Specification v2.0 `PEP
249 <https://www.python.org/dev/peps/pep-0249/>`__ for
`JSON-RPC <http://www.jsonrpc.org/specification>`__. Standart python
database api, but under the hood you make remote procedure call.

Install
-------

.. code:: bash

    pip install jsonrpcdb

Usage
-----

.. code:: python

    import jsonrpcdb

    # without authentication
    conn_params = {
        'host': 'ip/hostname',  # default localhost
        'port': 4000,  # default 4000
        'database': 'uri path', # default empty value
        'schema': 'http/https', # default http
    }

    # with token authentication
    conn_params = {
        'host': 'ip/hostname',
        'port': 4000,
        'database': 'uri path',
        'schema': 'http/https',
        'user': 'username',
        'password': 'password',
        'auth_type': 'token'
    }

    conn = jsonrpcdb.connect(**conn_params)
    cur = conn.cursor()
    data = {
        'params': {} # remote procedure parameters
    }
    cur.execute('some_method', data)
    results = cur.fetchall()

.. |Build Status| image:: https://travis-ci.org/LiveStalker/json-rpc-db.svg?branch=master
   :target: https://travis-ci.org/LiveStalker/json-rpc-db
.. |Codacy Badge| image:: https://api.codacy.com/project/badge/Coverage/52f1f4086b654639b78ffc0b28bb9b00
   :target: https://www.codacy.com/app/LiveStalker/json-rpc-db?utm_source=github.com&utm_medium=referral&utm_content=LiveStalker/json-rpc-db&utm_campaign=Badge_Coverage
.. |Codacy Badge| image:: https://api.codacy.com/project/badge/Grade/52f1f4086b654639b78ffc0b28bb9b00
   :target: https://www.codacy.com/app/LiveStalker/json-rpc-db?utm_source=github.com&utm_medium=referral&utm_content=LiveStalker/json-rpc-db&utm_campaign=Badge_Grade
