from flask_limiter.util import get_remote_address
from olive.proto.rpc import RPCClient
from flask_restful import Resource
from fig import app, limiter


class Client(Resource):
    """

    Rate limit is set based on the resource (Class) not per http method
    this limitation is discussed here:
        - https://github.com/alisaifee/flask-limiter/issues/11

    """
    decorators = [limiter.limit("10/minute", key_func=get_remote_address)]

    # method_decorators = {'get': [is_user_authorized]}

    def __init__(self):
        self.err = app.config['ERRORS']
        super(Client, self).__init__()

    def get(self):
        client_rpc = RPCClient('cranberry')
        res = client_rpc.call(method='VerifyAccessToken',
                              client_id='123',
                              access_token='A-SAMPLE-USER-ID:a58d4b5b8452499eab702150309ef675'
                              )
        return {}

    def post(self):
        pass
