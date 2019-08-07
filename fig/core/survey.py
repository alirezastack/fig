from flask_limiter.util import get_remote_address
from olive.proto.rpc import RPCClient
from flask_restful import Resource
from fig.schemas import add_survey
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
        raise NotImplementedError

    def post(self):
        app.logger.debug('creating a new survey...')
        survey = request.json
        app.logger.debug('survey payload: {}'.format(survey))
        validate(instance=survey, schema=add_survey)
        app.logger.debug('payload is valid, sending request to Mango...')
        client_rpc = RPCClient('mango')
        res = client_rpc.call(method='AddSurvey',
                              **survey)
        app.logger.info('survey has been created: {}'.format(res.survey_id))
        return {'survey_id': res.survey_id}, 201


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
        raise NotImplementedError

    def patch(self, survey_id):
        raise NotImplementedError

    def delete(self, survey_id):
        raise NotImplementedError
