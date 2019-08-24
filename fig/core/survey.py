from flask_limiter.util import get_remote_address
from olive.http import parse_get_args
from olive.proto.rpc import RPCClient
from fig.schemas import add_survey
from flask_restful import Resource
from fig.response import Response
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
        filters = parse_get_args(request, ['skip', 'page_size', 'city', 'complex'])

        app.logger.debug('getting list of surveys {}'.format(filters))
        client_rpc = RPCClient('mango')
        res = client_rpc.call(method='GetSurveys',
                              **filters)

        surveys = []
        for survey in res.surveys:
            surveys.append({
                '_id': survey._id,
                'reservation_id': survey.reservation_id,
                'total_rating': survey.total_rating,
                'questions': [{'question_id': q.question_id, 'rating': q.rating} for q in survey.questions],
                'staff_id': survey.staff_id,
                'user_id': survey.user_id,
                'status': survey.status,
                'content': survey.content,
                'platform': survey.platform
            })

        return Response.success(
            result=surveys,
            pagination={
                'skip': filters.get('skip', 0),
                'page_size': filters.get('page_size', 50),
                'total_count': res.total_count
            }
        )

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

        return Response.success(
            result={'survey_id': res.survey_id},
            status_code=201
        )


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
