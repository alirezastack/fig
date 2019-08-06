from flask_limiter.util import get_remote_address
from flask_restful import Resource
from fig import limiter


class Client(Resource):
    """

    Rate limit is set based on the resource (Class) not per http method
    this limitation is discussed here:
        - https://github.com/alisaifee/flask-limiter/issues/11

    """
    decorators = [limiter.limit("10/minute", key_func=get_remote_address)]

    # method_decorators = {'get': [is_user_authorized]}

    def __init__(self):
        super(Client, self).__init__()

    def get(self):
        pass

    def post(self):
        pass
