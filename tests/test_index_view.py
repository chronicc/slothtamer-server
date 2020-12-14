""" Test the index view. """

import json

from slothtamer.vars import APP_NAME, APP_VERSION


def test_index(client):
    """ Test if the index endpoint returns the correct code and response. """
    response = client.get('/')
    data = json.loads(response.get_data().decode('utf-8'))
    assert response.status_code == 200
    assert data['name'] == APP_NAME
    assert data['version'] == APP_VERSION
