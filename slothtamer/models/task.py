# pylint: disable=E1101
""" Task Model """

from datetime import datetime as dt
from datetime import timedelta as td
from datetime import timezone as tz
from pytz import utc
from sqlalchemy.orm import validates

from slothtamer.lib.database import db


class Task(db.Model):
    """ Task Model """

    __tablename__ = 'tasks'
    __table_args__ = {'sqlite_autoincrement': True}

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128), index=True)
    status = db.Column(db.Integer, default=0)
    _due_date = db.Column('due_date', db.DateTime, default=dt.now(tz=tz.utc) + td(days=1))
    _created = db.Column('created', db.DateTime, default=dt.now(tz=tz.utc))
    _updated = db.Column('updated', db.DateTime, default=dt.now(tz=tz.utc), onupdate=dt.now(tz.utc))

    def __repr__(self):
        return "<Task(id='%s', title='%s', status='%s')>" % (
            self.id, self.title, self.status)

    def to_dict(self):
        """ Return the whole task object as dictionary. """
        return dict(id=self.id, title=self.title, status=self.status,
                    dueDate=self.due_date, created=self.created, updated=self.updated)

    @property
    def due_date(self):
        """ Returns the utc normalized due date. """
        return utc.localize(self._due_date)

    @due_date.setter
    def due_date(self, due_date):
        """ Set the due_date. """
        self._due_date = due_date

    @property
    def created(self):
        """ Returns the utc normalized creation date. """
        return utc.localize(self._created)

    @property
    def updated(self):
        """ Returns the utc normalized update date. """
        return utc.localize(self._updated)

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

    @validates('_due_date')
    def validate_due_date(self, key, _due_date):
        """ Validates the due date parameter of the task object. """
        del key
        assert isinstance(_due_date, dt), 'Wrong format for due date'
        assert _due_date > dt.now(tz.utc), 'Due date must be in the future'
        return _due_date
    # pylint: enable=R0201
