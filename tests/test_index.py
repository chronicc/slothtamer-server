import json

from slothtamer.vars import APP_NAME, APP_VERSION


def test_index(client):
    """ Test if the index endpoint returns the correct code and response. """
    r = client.get('/')
    d = json.loads(r.get_data().decode('utf-8'))
    assert r.status_code == 200
    assert d['name'] == APP_NAME
    assert d['version'] == APP_VERSION
