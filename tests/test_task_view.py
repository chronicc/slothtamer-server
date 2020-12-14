""" Test the task view. """

import json

from datetime import datetime

from slothtamer.models.task import Task


def test_post(client, app):
    """ Test if a task can be created with minimal parameters. """
    title = 'Test Task'
    response = client.post('/tasks/', data={'title': title})
    data = json.loads(response.get_data().decode('utf-8'))
    assert response.status_code == 200
    assert data == 'OK'
    with app.app_context():
        assert Task.query.filter_by(title=title).first() is not None

# TODO: Finish task view testing.
def test_get_id(client):
    """ Test if a task can be retrieved with an id. """
    response = client.get('/tasks/1/')
    data = json.loads(response.get_data().decode('utf-8'))
    assert response.status_code == 200
    assert data['title'] == 'Test Task'
    assert data['status'] == 0
    assert isinstance(datetime.fromisoformat(data['created']), datetime)


# def test_task_create_wrong(client, app):
#     """ Test if the task view is safe against wrong methods."""
#     title = 'Don\'t accept wrong method'
#     client.get('/tasks/', data={'title': title})
#     with app.app_context():
#         assert Task.query.filter_by(title=title).first() is None
