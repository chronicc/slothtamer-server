""" Task View """

from flask import jsonify, request, make_response
from flask.views import MethodView
from flask_login import login_required

from slothtamer.models.task import Task


class TasksView(MethodView):
    """ Tasks View """

    @classmethod
    @login_required
    def get(cls, task_id=None):
        """ Return one or multiple tasks. """
        if task_id is None:
            return make_response(jsonify([row.to_dict() for row in Task.query.all()]))

        try:
            return make_response(jsonify(Task.read(task_id).to_dict()))
        except AttributeError:
            return make_response(jsonify('No task with id \'%s\' found' % task_id), 404)

    @classmethod
    @login_required
    def post(cls):
        """ Create a new task. """
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

    @classmethod
    @login_required
    def patch(cls, task_id):
        """ Change the properties of a task. """
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
            return make_response(jsonify('Nothing to update'), 200)

        try:
            Task.update(task_id, params)
        except AssertionError as err:
            return make_response(jsonify('Malformed request: %s' % err), 400)

        return jsonify('OK')

    @classmethod
    @login_required
    def delete(cls, task_id):
        """ Delete a task. """
        Task.delete(task_id)
        return make_response(jsonify('OK'))
