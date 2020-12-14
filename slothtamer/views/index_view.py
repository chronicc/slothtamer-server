from flask import jsonify, make_response
from flask.views import MethodView
from flask_login import login_required

from slothtamer.vars import APP_NAME, APP_VERSION


class IndexView(MethodView):
    """ Index View """

    @login_required
    def get(self):
        return make_response(jsonify(dict(name=APP_NAME, version=APP_VERSION)), 200)
