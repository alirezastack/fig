from fig.schemas import add_question, update_question
from flask_limiter.util import get_remote_address
from olive.proto.rpc import RPCClient
from flask_restful import Resource
from fig.response import Response
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
        client_rpc = RPCClient('mango')
        res = client_rpc.call(method='GetQuestions')
        questions = []
        for question in res.questions:
            questions.append({
                '_id': question._id,
                'title': {
                    'on_rate': question.title.on_rate,
                    'on_display': question.title.on_display
                },
                'order': question.order,
                'status': question.status,
                'include_in': list(question.include_in),
                'weight': question.weight
            })

        return Response.success(
            result=questions,
        )

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
        return Response.success(
            result={'question_id': res.question_id},
            status_code=201
        )


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

        return Response.success(
            result={
                '_id': res._id,
                'title': {
                    'on_rate': res.title.on_rate,
                    'on_display': res.title.on_display
                },
                'order': res.order,
                'status': res.status,
                'include_in': list(res.include_in),
                'weight': res.weight
            }
        )

    def patch(self, question_id):
        app.logger.debug('patch question {}'.format(question_id))
        question = request.json
        validate(instance=question, schema=update_question)
        app.logger.debug('payload valid, sending request to Mango...')
        client_rpc = RPCClient('mango')
        res = client_rpc.call(method='UpdateQuestion',
                              question_id=question_id,
                              **question)

        return Response.success(
            result={'is_updated': res.is_updated}
        )

    def delete(self, question_id):
        app.logger.debug('deleting question {}...'.format(question_id))
        client_rpc = RPCClient('mango')
        res = client_rpc.call(method='DeleteQuestion',
                              question_id=question_id)

        return Response.success(
            result={'is_deleted': res.is_deleted}
        )
