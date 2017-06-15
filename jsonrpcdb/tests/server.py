from werkzeug.wrappers import Response, Request
from werkzeug.serving import run_simple

from jsonrpc import JSONRPCResponseManager, dispatcher


@dispatcher.add_method
def login(**kwargs):
    username = kwargs['user']
    password = kwargs['password']
    if username == 'test' and password == 'test':
        return 'success_token'
    else:
        # TODO return error
        return False


@Request.application
def app(request):
    dispatcher['scalar'] = lambda a: a
    dispatcher['list_of_scalar'] = lambda a: [a, a, a]
    dispatcher['list_of_list'] = lambda a: [[a, a, a], [a, a, a], [a, a, a]]
    dispatcher['list_of_dict'] = lambda a: [{'a': a}, {'a': a}, {'a': a}]

    response = JSONRPCResponseManager.handle(request.data, dispatcher)
    return Response(response.json, mimetype='application/json')


if __name__ == '__main__':
    run_simple('localhost', 4000, app)
