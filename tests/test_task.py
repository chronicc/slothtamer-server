""" Test the task view. """

import json

from datetime import datetime

from slothtamer.models.task import Task


TASKS_ROUTE = '/tasks/'
TASK_ROUTE = '/tasks/1/'


def test_task_lifecycle(client, app):
    """ Test the full lifecycle of a task from creation to deletion. """
    title = 'Foobar'

    # POST
    response = client.post(TASKS_ROUTE, data={'title': title})
    data = json.loads(response.get_data().decode('utf-8'))
    assert response.status_code == 200
    assert data == 'OK'
    with app.app_context():
        task = Task.query.filter_by(title=title).first()
        assert str(task) == '<Task(id=\'1\', title=\'%s\', status=\'0\')>' % title

    # GET id
    response = client.get(TASK_ROUTE)
    data = json.loads(response.get_data().decode('utf-8'))
    assert response.status_code == 200
    assert data['id'] == 1
    assert data['title'] == title
    assert data['status'] == 0
    assert isinstance(datetime.fromisoformat(data['created']), datetime)
    assert isinstance(datetime.fromisoformat(data['updated']), datetime)

    # GET list
    response = client.get(TASKS_ROUTE)
    data = json.loads(response.get_data().decode('utf-8'))
    assert response.status_code == 200
    assert data != []

    # PATCH
    response = client.patch(TASK_ROUTE, data={'status': 1})
    data = json.loads(response.get_data().decode('utf-8'))
    assert response.status_code == 200
    assert data == 'OK'
    response = client.patch(TASK_ROUTE, data={'title': 'Fubar'})
    data = json.loads(response.get_data().decode('utf-8'))
    assert response.status_code == 200
    assert data == 'OK'
    with app.app_context():
        assert Task.query.filter_by(title='Fubar').first().status == 1

    # PATCH malformed
    response = client.patch(TASK_ROUTE, data={'status': ''})
    data = json.loads(response.get_data().decode('utf-8'))
    assert response.status_code == 400
    assert data.startswith('Malformed request:')

    # PATCH no change
    response = client.patch(TASK_ROUTE, data={})
    data = json.loads(response.get_data().decode('utf-8'))
    assert response.status_code == 200
    assert data == 'Nothing to update'

    # DELETE
    response = client.delete(TASK_ROUTE)
    data = json.loads(response.get_data().decode('utf-8'))
    assert response.status_code == 200
    assert data == 'OK'
    with app.app_context():
        assert Task.query.filter_by(title=title).first() is None


def test_task_not_found_error(client):
    """ Test if correct error is returned when no task is found. """
    response = client.get(TASK_ROUTE)
    data = json.loads(response.get_data().decode('utf-8'))
    assert response.status_code == 404
    assert data == 'No task with id \'1\' found'


def test_task_without_title_error(client):
    """ Test if correct error is returned from task view when task is created without a title. """
    response = client.post(TASKS_ROUTE)
    data = json.loads(response.get_data().decode('utf-8'))
    assert response.status_code == 400
    assert data == 'Title missing in request'


def test_task_malformed_request_on_create(client):
    """ Test validation if task fields. """

    # Empty status
    response = client.post(TASKS_ROUTE, data={'title': 'Foobar', 'status': ''})
    data = json.loads(response.get_data().decode('utf-8'))
    assert response.status_code == 400
    assert data == ('Malformed request: Status must not be empty')

    # Non convertable to integer
    response = client.post(TASKS_ROUTE, data={'title': 'Foobar', 'status': 'Foobar'})
    data = json.loads(response.get_data().decode('utf-8'))
    assert response.status_code == 400
    assert data == ('Malformed request: Can\'t convert status to type integer')

    # Negative number
    response = client.post(TASKS_ROUTE, data={'title': 'Foobar', 'status': -1})
    data = json.loads(response.get_data().decode('utf-8'))
    assert response.status_code == 400
    assert data == ('Malformed request: Status must be a positive integer')


# def test_task_create_wrong(client, app):
#     """ Test if the task view is safe against wrong methods."""
#     title = 'Don\'t accept wrong method'
#     client.get('/tasks/', data={'title': title})
#     with app.app_context():
#         assert Task.query.filter_by(title=title).first() is None
