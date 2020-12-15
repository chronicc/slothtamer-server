""" Test the user model and view. """

from slothtamer.models.user import User


def test_user_repr(app):
    """ Test if the model is represented in the correct form. """
    with app.app_context():
        user = User.query.first()
        assert str(user) == '<User(id=\'1\', api_key=\'testing\')>'


def test_user_to_dict(app):
    """ Test if the model is returned as dict. """
    with app.app_context():
        data = User.query.first().to_dict()
        assert isinstance(data, dict)
        assert data['id'] == 1
