from fig.fig_app import FigApp
import pytest


@pytest.fixture
def app():
    app = FigApp().setup()
    yield app


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def runner(app):
    return app.test_cli_runner()


def test_get_cart(client, app):
    assert client.get('/cart').status_code == 200
