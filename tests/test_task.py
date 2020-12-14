""" Test the task view. """

import json

from slothtamer.models.task import Task


def test_task_create_minimal(client, app):
    """ Test if a task can be created with minimal parameters. """
    title = 'Test task object'
    response = client.post('/tasks/', data={'title': title})
    data = json.loads(response.get_data().decode('utf-8'))
    assert response.status_code == 200
    assert data == 'OK'
    with app.app_context():
        assert Task.query.filter_by(title=title).first() is not None


def test_task_create_wrong(client, app):
    """ Test if the task view is safe against wrong methods."""
    title = 'Don\'t accept wrong method'
    client.get('/tasks/', data={'title': title})
    with app.app_context():
        assert Task.query.filter_by(title=title).first() is None
