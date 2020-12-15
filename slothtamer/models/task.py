# pylint: disable=E1101
""" Task Model """

from datetime import datetime as dt
from datetime import timezone as tz
from sqlalchemy.orm import validates

from slothtamer.lib.database import db


class Task(db.Model):
    """ Task Model """

    __tablename__ = 'tasks'
    __table_args__ = {'sqlite_autoincrement': True}

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128), index=True)
    status = db.Column(db.Integer, default=0)
    created = db.Column(db.DateTime, default=dt.now(tz.utc))
    updated = db.Column(db.DateTime, default=dt.now(tz.utc), onupdate=dt.now(tz.utc))

    def __repr__(self):
        return "<Task(id='%s', title='%s', status='%s')>" % (
            self.id, self.title, self.status)

    def to_dict(self):
        """ Return the whole task object as dictionary. """
        return dict(id=self.id, title=self.title, status=self.status,
                    created=self.created.isoformat(), updated=self.updated.isoformat())

    @classmethod
    def create(cls, params):
        """ Create a task object in the database. """
        task = Task(**params)
        db.session.add(task)
        db.session.commit()

    @classmethod
    def read(cls, task_id):
        """ Return a task object from the database. """
        return Task.query.filter_by(id=task_id).first()

    @classmethod
    def update(cls, task_id, params):
        """ Change a task object in the database. """
        task = Task.read(task_id)
        for key, value in params.items():
            setattr(task, key, value)
        db.session.commit()

    @classmethod
    def delete(cls, task_id):
        """ Remove a task object from the database. """
        task = Task.read(task_id)
        db.session.delete(task)
        db.session.commit()

    # pylint: disable=R0201
    @validates('title')
    def validate_title(self, key, title):
        """ Validate the title parameter of the task object. """
        del key
        assert title != '', 'Title must not be empty'
        return str(title)

    @validates('status')
    def validate_status(self, key, status):
        """ Validate the status parameter of the task object. """
        del key
        assert status != '', 'Status must not be empty'
        try:
            status = int(status)
        except ValueError as exception:
            raise AssertionError('Can\'t convert status to type integer') from exception
        assert status >= 0, 'Status must be a positive integer'
        return status
    # pylint: enable=R0201
