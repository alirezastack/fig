from olive.proto.rpc import RPCClient
from unittest.mock import patch
from fig.fig_app import FigApp
import ujson as json
import pytest


class MockQuestionResponse(object):
    def __init__(self, _id, ranges, weight, title, order, category, status, include_in):
        self._id = _id
        self.question_id = _id
        self.ranges = ranges
        self.weight = weight
        self.title = title
        self.order = order
        self.category = category
        self.status = status
        self.include_in = include_in


class MockRanges(object):
    def __init__(self, color, range, content):
        self.color = color
        self.range = range
        self.content = content


class MockTitle(object):
    def __init__(self, on_rate, on_display):
        self.on_rate = on_rate
        self.on_display = on_display


class MockQuestionDeletion(object):
    def __init__(self, is_deleted):
        self.is_deleted = is_deleted


class MockQuestionUpdate(object):
    def __init__(self, is_updated):
        self.is_updated = is_updated


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


@patch.object(RPCClient, 'call')
def test_create_question(mock_rpc_resp, client, app):
    mock_rpc_resp.return_value = MockQuestionResponse(
        _id='5d47b9b46dd9f292c39362c8',
        title=MockTitle('rateeee', 'displaeeee'),
        weight=1,
        order=1,
        ranges=[MockRanges('#000', '(1,3)', 'Great')],
        category='cate',
        status='active',
        include_in=['on_rate', 'on_display']
    )

    mimetype = 'application/json'
    headers = {
        'Content-Type': mimetype,
        'Accept': mimetype
    }

    response = client.post('/questions', data=json.dumps({
        'order': 1,
        'title': {
            'on_rate': '',
            'on_display': ''
        },
        'include_in': ['on_rate'],
        'weight': 1,
        'status': 'active',
        'category': 'h'
    }), headers=headers)

    assert response.json['question_id'] == '5d47b9b46dd9f292c39362c8'
    assert type(response.json['question_id']) == str


@patch.object(RPCClient, 'call')
def test_create_invalid_includein_question(mock_rpc_resp, client, app):
    mock_rpc_resp.return_value = MockQuestionResponse(
        _id='5d47b9b46dd9f292c39362c8',
        title=MockTitle('rateeee', 'displaeeee'),
        weight=1,
        order=1,
        ranges=[MockRanges('#000', '(1,3)', 'Great')],
        category='cate',
        status='active',
        include_in=['on_rate']
    )

    mimetype = 'application/json'
    headers = {
        'Content-Type': mimetype,
        'Accept': mimetype
    }

    response = client.post('/questions', data=json.dumps({
        'order': 1,
        'title': {
            'on_rate': '',
            'on_display': ''
        },
        'include_in': ['on_rate', 'on_rate'],
        'weight': 1,
        'status': 'active',
        'category': 'h'
    }), headers=headers)

    assert response.status_code == 400
    assert response.json['error']['code'] == 'invalid_schema'
    assert 'non-unique' in response.json['error']['reason']


@patch.object(RPCClient, 'call')
def test_delete_question(mock_rpc_resp, client, app):
    mock_rpc_resp.return_value = MockQuestionDeletion(
        is_deleted=True
    )

    response = client.delete('/questions/5d47b9b46dd9f292c39362c8')

    assert response.status_code == 200
    assert type(response.json['is_deleted']) == bool
    assert response.json['is_deleted'] == True


@patch.object(RPCClient, 'call')
def test_update_question(mock_rpc_resp, client, app):
    mock_rpc_resp.return_value = MockQuestionUpdate(
        is_updated=True
    )

    mimetype = 'application/json'
    headers = {
        'Content-Type': mimetype,
        'Accept': mimetype
    }
    response = client.patch('/questions/5d47b9b46dd9f292c39362c8', data=json.dumps({
        'title': {
            'on_rate': '',
            'on_display': ''
        }
    }), headers=headers)

    assert response.status_code == 200
    assert type(response.json['is_updated']) == bool
    assert response.json['is_updated'] == True


def test_min_properties_update_question(client, app):
    mimetype = 'application/json'
    headers = {
        'Content-Type': mimetype,
        'Accept': mimetype
    }
    response = client.patch(path='/questions/5d47b9b46dd9f292c39362c8',
                            data=json.dumps({}),
                            headers=headers)

    assert response.status_code == 400
    assert 'does not have enough properties' in response.json['error']['reason']


def test_invalid_properties_update_question(client, app):
    mimetype = 'application/json'
    headers = {
        'Content-Type': mimetype,
        'Accept': mimetype
    }
    response = client.patch(path='/questions/5d47b9b46dd9f292c39362c8',
                            data=json.dumps({'invalid_prop': 'some_value'}),
                            headers=headers)

    assert response.status_code == 400
    assert 'Additional properties are not allowed' in response.json['error']['reason']


# TODO not working! needs to be fixed
# some_error_mock = mock.Mock()
# some_error_mock.side_effect = GRPCError(
#     message='Document `blah` not found!',
#     errors={
#         'code': 'resource_not_found',
#         'details': [],
#         'message': 'Document `blah` not found!'
#     }
# )
#
#
# @patch.object(RPCClient, 'call', some_error_mock)
# def test_get_404_question(client):
#     with pytest.raises(GRPCError):
#         assert client.get('/questions/non_existent_question')
