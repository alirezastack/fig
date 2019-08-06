from fig.schemas import add_question, update_question
from flask_limiter.util import get_remote_address
from olive.proto.rpc import RPCClient
from flask_restful import Resource
from jsonschema import validate
from fig import app, limiter
from flask import request


class QuestionCollection(Resource):
    """

    Rate limit is set based on the resource (Class) not per http method
    this limitation is discussed here:
        - https://github.com/alisaifee/flask-limiter/issues/11

    """
    decorators = [limiter.limit("10/minute", key_func=get_remote_address)]

    # method_decorators = {'get': [is_user_authorized]}

    def __init__(self):
        super(QuestionCollection, self).__init__()

    def get(self):
        # TODO to be implemented
        client_rpc = RPCClient('mango')
        res = client_rpc.call(method='GetQuestions')
        print(res)
        return {}

    def post(self):
        app.logger.debug('creating a new question...')
        question = request.json
        app.logger.debug('question payload: {}'.format(question))
        validate(instance=question, schema=add_question)
        app.logger.debug('payload valid, sending request to Mango...')
        client_rpc = RPCClient('mango')
        res = client_rpc.call(method='AddQuestion',
                              **question)
        app.logger.info('question has been created: {}'.format(res.question_id))
        return {'question_id': res.question_id}, 201


class QuestionResource(Resource):
    """

    Rate limit is set based on the resource (Class) not per http method
    this limitation is discussed here:
        - https://github.com/alisaifee/flask-limiter/issues/11
        - https://github.com/alisaifee/flask-limiter/issues/11#issuecomment-68080840

    """
    decorators = [limiter.limit("10/minute", key_func=get_remote_address)]

    # method_decorators = {'get': [is_user_authorized]}

    def __init__(self):
        super(QuestionResource, self).__init__()

    def get(self, question_id):
        client_rpc = RPCClient('mango')
        res = client_rpc.call(method='GetQuestionById',
                              question_id=question_id)

        ranges = []
        for r in res.ranges[:]:
            ranges.append({
                'color': r.color,
                'range': r.range,
                'content': r.content
            })

        return {
            '_id': res._id,
            'ranges': ranges,
            'category': res.category,
            'title': {
                'on_rate': res.title.on_rate,
                'on_display': res.title.on_display
            },
            'order': res.order,
            'status': res.status,
            'include_in': list(res.include_in),
            'weight': res.weight
        }

    def patch(self, question_id):
        app.logger.debug('patch question {}'.format(question_id))
        question = request.json
        validate(instance=question, schema=update_question)
        app.logger.debug('payload valid, sending request to Mango...')
        client_rpc = RPCClient('mango')
        res = client_rpc.call(method='UpdateQuestion',
                              question_id=question_id,
                              **question)
        return {
            'is_updated': res.is_updated
        }

    def delete(self, question_id):
        client_rpc = RPCClient('mango')
        res = client_rpc.call(method='DeleteQuestion',
                              question_id=question_id)
        return {
            'is_deleted': res.is_deleted
        }
