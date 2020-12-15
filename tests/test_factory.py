""" Test the application factory. """

import os
import shutil

from slothtamer import config_set_default, create_app


def test_environment_configuration():
    """ Test the usage of environment variables. """
    os.environ['TEST_ENV'] = 'Foo'
    assert config_set_default('TEST_ENV', 'Bar') == 'Foo'


def test_without_config():
    """ Test application creation without config parameter. """
    app = create_app()
    assert app.config['API_KEY'] == 'insecure'
    assert app.config['SQLALCHEMY_DATABASE_URI'] == 'sqlite:///:memory:'
    assert not app.testing
    shutil.rmtree(app.instance_path)


def test_with_config():
    """ Test application creation with a prepared config parameter. """
    config = {
        'API_KEY': 'testing',
        'TESTING': True,
        'SQLALCHEMY_DATABASE_URI': 'sqlite:////tmp/instance/slothtamer.db',
        'SQLALCHEMY_TRACK_MODIFICATIONS': False,
    }
    app = create_app(config, instance_path='/tmp/instance')
    del app
    app = create_app(config, instance_path='/tmp/instance')
    assert app.config['API_KEY'] == 'testing'
    assert app.config['SQLALCHEMY_DATABASE_URI'] == 'sqlite:////tmp/instance/slothtamer.db'
    assert app.testing
