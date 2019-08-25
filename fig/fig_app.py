from fig.core.question import QuestionCollection, QuestionResource
from fig.core.survey import SurveyCollection, SurveyResource
from flask_graphql import GraphQLView
from fig.core.client import Client
from fig.schema import GraphSchema
from fig.core.login import ROPC
from flask_restful import Api
from fig import app


class FigApp:
    def setup(self):
        api = Api(app)

        # ************* Cranberry Endpoints *************
        api.add_resource(ROPC, '/oauth/token')
        api.add_resource(Client, '/oauth/client')

        # ************* Mango Endpoints *************
        api.add_resource(QuestionCollection, '/questions')
        api.add_resource(QuestionResource, '/questions/<string:question_id>')
        api.add_resource(SurveyCollection, '/surveys')
        api.add_resource(SurveyResource, '/surveys/<string:survey_id>')

        app.add_url_rule('/graphql', view_func=GraphQLView.as_view('graphql', schema=GraphSchema, graphiql=True))

        return app
