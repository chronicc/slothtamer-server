""" Test the task model and view. """

import json

from slothtamer.lib.database import db
from slothtamer.models.task import Task


# def test_task_repr(client, app):
#     """ Test if the model is represented in the correct form. """
#     with app.app_context():
#         task = Task.query.first()
#         assert str(task) == '<Task(id=\'1\', title=\'Test task object\', status=\'0\')>'


def test_task_to_dict(client, app):
    """ Test if the model is returned as dict. """
    with app.app_context():
        db.session.add(Task(title='Example Task'))
        db.session.commit()
        data = Task.query.first().to_dict()
        assert isinstance(data, dict)
        assert data['id'] == 1
        assert data['title'] == 'Example Task'
        assert data['status'] == 0
