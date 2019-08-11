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


class MockGetSurveysResponse(object):
    def __init__(self, id, reservation_id, total_rating, questions, staff_id, user_id, status, content, platform, total_count):
        self._id = id
        self.reservation_id = reservation_id
        self.total_rating = total_rating
        self.questions = questions
        self.staff_id = staff_id
        self.user_id = user_id
        self.status = status
        self.content = content
        self.platform = platform


class MockSurveyQuestions(object):
    def __init__(self, question_id, rating):
        self.question_id = question_id
        self.rating = rating


class MockSurveysResponse(object):
    def __init__(self, surveys, total_count):
        self.surveys = surveys
        self.total_count = total_count


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


@patch.object(RPCClient, 'call')
def test_get_surveys(mock_rpc_resp, client, app):
    mock_rpc_resp.return_value = MockSurveysResponse(surveys=[MockGetSurveysResponse(total_count=20,
                                                                                     id='1231231233',
                                                                                     total_rating=10,
                                                                                     questions=[MockSurveyQuestions('q1', 2),
                                                                                                MockSurveyQuestions('q2', 3)],
                                                                                     staff_id='ads',
                                                                                     user_id='sdff',
                                                                                     status='sddd',
                                                                                     platform='das',
                                                                                     reservation_id='asdas',
                                                                                     content='sds')],
                                                     total_count=12)

    response = client.get(path='/surveys')

    assert len(response.json['result']) == 1
    assert response.status_code == 200
    assert 'pagination' in response.json
    assert type(response.json['result']) == list
