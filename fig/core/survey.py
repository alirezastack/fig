from flask_limiter.util import get_remote_address
from olive.proto.rpc import RPCClient
from flask_restful import Resource
from jsonschema import validate
from fig import app, limiter
from flask import request


class SurveyCollection(Resource):
    """

    Rate limit is set based on the resource (Class) not per http method
    this limitation is discussed here:
        - https://github.com/alisaifee/flask-limiter/issues/11

    """
    decorators = [limiter.limit("10/minute", key_func=get_remote_address)]

    # method_decorators = {'get': [is_user_authorized]}

    def __init__(self):
        super(SurveyCollection, self).__init__()

    def get(self):
        # TODO to be implemented
        pass

    def post(self):
        # TODO to be implemented
        return {}, 201


class SurveyResource(Resource):
    """

    Rate limit is set based on the resource (Class) not per http method
    this limitation is discussed here:
        - https://github.com/alisaifee/flask-limiter/issues/11
        - https://github.com/alisaifee/flask-limiter/issues/11#issuecomment-68080840

    """
    decorators = [limiter.limit("10/minute", key_func=get_remote_address)]

    # method_decorators = {'get': [is_user_authorized]}

    def __init__(self):
        super(SurveyResource, self).__init__()

    def get(self, survey_id):
        # TODO to be implemented
        pass

    def patch(self, survey_id):
        # TODO to be implemented
        pass

    def delete(self, survey_id):
        # TODO to be implemented
        pass
