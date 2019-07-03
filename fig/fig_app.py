from fig.core.client import Client
from fig.core.login import ROPC
from flask_restful import Api
from fig import app


class FigApp:
    def setup(self):
        api = Api(app)

        # ************* Cranberry Endpoints *************
        temp_base_path = '/oauth'
        api.add_resource(ROPC, '{}/login'.format(temp_base_path))
        api.add_resource(Client, '{}/client'.format(temp_base_path))

        return app
