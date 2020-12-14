# pylint: disable=E1101
""" Slothtamer Application """

import os

from flask import Flask
from flask_login import LoginManager

from slothtamer.lib.database import db
from slothtamer.models.task import Task
from slothtamer.models.user import User
from slothtamer.views.index_view import IndexView
from slothtamer.views.tasks_view import TasksView


def config_set_default(param, default):
    """ Return the value of an environment variable or default if not defined."""
    if param in os.environ:
        return os.environ[param]
    return default


def create_app(config=None):
    """ Create an instance of the application. """

    # Application
    app = Flask(__name__)

    if config is None:
        config_mapping = {
            'API_KEY': config_set_default('SLOTHTAMER_API_KEY', 'insecure'),
            'DEBUG': config_set_default('SLOTHTAMER_DEBUG', True),
            'SECRET_KEY': config_set_default('SLOTHTAMER_SECRET_KEY', os.urandom(16)),
            'SQLALCHEMY_DATABASE_URI': config_set_default(
                'SLOTHTAMER_DATABASE_URI', 'sqlite:///%s/slothtamer.db' % app.instance_path),
            'SQLALCHEMY_TRACK_MODIFICATIONS': False,
        }
    else:
        config_mapping = config
    app.config.from_mapping(config_mapping)

    print('INFO: Checking for application instance path: %s' % app.instance_path)
    try:
        os.makedirs(app.instance_path)
    except OSError:
        print('INFO: Application instance path already existing.')
    else:
        print('INFO: Application instance path created.')

    # Database
    db.init_app(app)
    if os.path.exists(os.path.join(app.instance_path, 'slothtamer.db')):
        print('INFO: Found a database file.')
    else:
        print('INFO: No database file found. Initializing database.')
        with app.app_context():
            db.create_all()
            # noinspection PyArgumentList
            db.session.add(User(api_key=app.config['API_KEY']))
            db.session.commit()
        print('INFO: Database initialized.')

    # Authorization
    auth = LoginManager()
    auth.init_app(app)

    @auth.request_loader
    def _request_loader(request):
        api_key = request.headers.get('Authorization')
        return User.query.filter_by(api_key=api_key).first()

    # Routes
    app.add_url_rule('/', view_func=IndexView.as_view('index'))
    app.add_url_rule('/tasks/', view_func=TasksView.as_view('tasks'))
    app.add_url_rule('/tasks/<int:id>/', view_func=TasksView.as_view('tasks_id'))

    return app
