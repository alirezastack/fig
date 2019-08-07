from olive.proto.rpc import RPCClient
from unittest.mock import patch
from fig.fig_app import FigApp
import pytest
import json


@pytest.fixture
def app():
    app = FigApp().setup()
    yield app


@pytest.fixture
def client(app):
    app.config['DEBUG'] = True
    app.config['TESTING'] = True
    return app.test_client()


@pytest.fixture
def runner(app):
    return app.test_cli_runner()


class MockSurveyResponse(object):
    def __init__(self, survey_id):
        self.survey_id = survey_id


@patch.object(RPCClient, 'call')
def test_create_survey(mock_rpc_resp, client, app):
    mock_rpc_resp.return_value = MockSurveyResponse(
        survey_id='5d47b9b46dd9f292c39362c8',
    )

    mimetype = 'application/json'
    headers = {
        'Content-Type': mimetype,
        'Accept': mimetype
    }
    response = client.post(path='/surveys', data=json.dumps({
        'user_id': '0d47b9b46dd9f292c39362c0',
        'staff_id': '0d47b9b46dd9f292c39362c0',
        'reservation_id': '5d47b9b46dd9f292c39362c8',
        'questions': [{
            'question_id': '12',
            'rating': 2
        }],
        'status': 'inactive',
        'content': 'test from all',
        'platform': 'android'
    }), headers=headers)

    assert response.status_code == 201
    assert 'survey_id' in response.json
    assert type(response.json['survey_id']) == str
