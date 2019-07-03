from flask_limiter.util import get_remote_address
from olive.proto.rpc_client import RPCClient
from flask_restful import Resource
from fig import app, limiter


class ROPC(Resource):
    """

    Rate limit is set based on the resource (Class) not per http method
    this limitation is discussed here:
        - https://github.com/alisaifee/flask-limiter/issues/11

    """
    decorators = [limiter.limit("10/minute", key_func=get_remote_address)]

    # method_decorators = {'get': [is_user_authorized]}

    def __init__(self):
        self.err = app.config['ERRORS']
        super(ROPC, self).__init__()

    def get(self):
        cart_client = RPCClient('cranberry')
        res = cart_client.call(method='ResourceOwnerPasswordCredential',
                               client_id='123',
                               client_secret='1232!!!!',
                               username='ali',
                               password='4321fddd',
                               scope='all')
        return {
            'access_token': res.access_token,
            'refresh_token': res.refresh_token,
            'expires_in': res.expires_in,
            'scope': res.scope,
        }

    def post(self):
        pass
