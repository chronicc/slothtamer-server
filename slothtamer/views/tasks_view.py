from flask import jsonify, request, make_response
from flask.views import MethodView
from flask_login import login_required

from slothtamer.models.task import Task


class TasksView(MethodView):
    """ Tasks View """

    @login_required
    def get(self, id=None):
        if id == None:
            return make_response(jsonify([row.to_dict() for row in Task.query.all()]))
        else:
            return make_response(jsonify(Task.read(id).to_dict()))


    @login_required
    def post(self):
        params = dict()

        try:
            params['title'] = request.form['title']
        except KeyError:
            return make_response(jsonify('Title missing in request'), 400)
        
        try:
            params['status'] = request.form['status']
        except KeyError:
            pass

        try:
            Task.create(params)
        except AssertionError as err:
            return make_response(jsonify('Malformed request: %s' % err), 400)

        return make_response(jsonify('OK'))


    @login_required
    def patch(self, id):
        params = dict()

        try:
            params['title'] = request.form['title']
        except KeyError:
            pass
        
        try:
            params['status'] = request.form['status']
        except KeyError:
            pass

        if len(params) == 0:
            return make_response(jsonify('Nothing to update'))
        
        try:
            Task.update(id, params)
        except AssertionError as err:
            return make_response(jsonify('Malformed request: %s' % err), 400)

        return jsonify('OK')


    @login_required
    def delete(self, id):
        Task.delete(id)
        return make_response(jsonify('OK'))
