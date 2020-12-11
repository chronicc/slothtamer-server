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
        return dict(id=self.id, title=self.title, status=self.status,
                    created=self.created.isoformat(), updated=self.updated.isoformat())


    @classmethod
    def create(cls, params):
        task = Task(**params)
        db.session.add(task)
        db.session.commit()


    @classmethod
    def read(cls, id):
        return Task.query.filter_by(id=id).first()


    @classmethod
    def update(cls, id, params):
        task = Task.read(id)
        for key, value in params.items():
            setattr(task, key, value)
        db.session.commit()


    @classmethod
    def delete(cls, id):
        task = Task.read(id)
        db.session.delete(task)
        db.session.commit()


    @validates('title')
    def validate_title(self, key, title):
        assert title != '', 'Title must not be empty'
        try:
            title = str(title)
        except ValueError:
            raise AssertionError('Title must be of type string')
        return title


    @validates('status')
    def validate_status(self, key, status):
        assert status != '', 'Status must not be empty'
        try:
            status = int(status)
        except ValueError:
            raise AssertionError('Status must be of type integer')
        assert status >= 0, 'Status must be a positive integer'
        return status
