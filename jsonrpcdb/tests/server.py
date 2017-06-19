import json
from werkzeug.wrappers import Response, Request
from werkzeug.serving import run_simple

from jsonrpc import JSONRPCResponseManager, dispatcher
from jsonrpc.jsonrpc2 import JSONRPC20Request

JSONRPC20Request.POSSIBLE_FIELDS.add('auth')
SUCCESS_TOKEN = 'success_token'

@dispatcher.add_method
def login(**kwargs):
    username = kwargs['user']
    password = kwargs['password']
    if username == 'test' and password == 'test':
        return SUCCESS_TOKEN
    else:
        # TODO return error
        return False


@Request.application
def app(request):
    json_request = json.loads(request.data)
    dispatcher['scalar'] = lambda a: a
    dispatcher['list_of_scalar'] = lambda a: [a, a, a]
    dispatcher['list_of_list'] = lambda a: [[a, a, a], [a, a, a], [a, a, a]]
    dispatcher['list_of_dict'] = lambda a: [{'a': a}, {'a': a}, {'a': a}]

    # emulate protected resource
    token = json_request.get('auth', None)
    if token == SUCCESS_TOKEN:
        dispatcher['protected_res'] = lambda a: [a, a, a]

    response = JSONRPCResponseManager.handle(request.data, dispatcher)
    return Response(response.json, mimetype='application/json')


if __name__ == '__main__':
    run_simple('localhost', 4000, app)
