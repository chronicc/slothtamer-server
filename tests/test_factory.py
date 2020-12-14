""" Test the application factory. """

import os
import shutil

from slothtamer import config_set_default, create_app


DATABASE_PATH = 'sqlite:///:memory:'


def test_environment_configuration():
    """ Test the usage of environment variables. """
    os.environ['TEST_ENV'] = 'Foo'
    assert config_set_default('TEST_ENV', 'Bar') == 'Foo'


def test_without_config():
    """ Test application creation without config parameter. """
    app = create_app()
    assert app.config['API_KEY'] == 'insecure'
    assert app.config['SQLALCHEMY_DATABASE_URI'] == DATABASE_PATH
    assert not app.testing
    shutil.rmtree(app.instance_path)


def test_with_config():
    """ Test application creation with a prepared config parameter. """
    config = {
        'API_KEY': 'testing',
        'TESTING': True,
        'SQLALCHEMY_DATABASE_URI': DATABASE_PATH,
        'SQLALCHEMY_TRACK_MODIFICATIONS': False,
    }
    app = create_app(config)
    assert app.config['API_KEY'] == 'testing'
    assert app.config['SQLALCHEMY_DATABASE_URI'] == DATABASE_PATH
    assert app.testing
