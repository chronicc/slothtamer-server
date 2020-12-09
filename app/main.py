import json
import os
import sys

from configparser import ConfigParser

from app import app, auth, db
from app.views.index_view import IndexView
from app.views.tasks_view import TasksView
from app.models.user import User

# Get Flask Default Config
# for key in app.config.keys:
#     print('%s: %s' % (key, app.config.get(key)))

# Config
try:
    with open('/etc/slothtamer/server.json', 'r') as fp:
        app.config.from_json(fp, False)
except FileNotFoundError:
    app.config['ENV'] = 'development'
    app.config['DEBUG'] = True
    app.config['SECRET_KEY'] = os.urandom(16)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


# Initialization
auth.init_app(app)
db.init_app(app)
app.app_context().push()
db.create_all()


# Generate admin user
user = User(api_key=os.environ['SLOTHTAMER_API_KEY'])
db.session.add(user)
db.session.commit()


# Authorization
@auth.request_loader
def request_loader(request):
    api_key = request.headers.get('Authorization')
    return User.query.filter_by(api_key=api_key).first()


# Routes
app.add_url_rule('/', view_func=IndexView.as_view('index'))
app.add_url_rule('/tasks/', view_func=TasksView.as_view('tasks'))
app.add_url_rule('/tasks/<int:id>/', view_func=TasksView.as_view('tasks_id'))
