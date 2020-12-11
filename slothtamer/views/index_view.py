from flask import jsonify, make_response
from flask.views import MethodView
from flask_login import login_required


class IndexView(MethodView):
    """ Index View """

    @login_required
    def get(self):
        return make_response(jsonify(dict(name='slothtamer', version='dev')), 200)
