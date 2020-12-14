import pytest

from flask.testing import FlaskClient

from slothtamer import create_app


class TestClient(FlaskClient):
    """ Special test client for local testing. """
    def open(self, *args, **kwargs):
        kwargs['headers'] = dict(Authorization='testing')
        return super().open(*args, **kwargs)


@pytest.fixture
def app():
    """ Create an application instance for local testing. """
    app = create_app({
        'API_KEY': 'testing',
        'TESTING': True,
        'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:',
        'SQLALCHEMY_TRACK_MODIFICATIONS': False,
    })

    yield app


@pytest.fixture
def client(app):
    """ Provide a simulated http client for local testing. """
    app.test_client_class = TestClient
    return app.test_client()


@pytest.fixture
def runner(app):
    """ Provide a simulated cli client for local testing. """
    return app.test_cli_runner()
