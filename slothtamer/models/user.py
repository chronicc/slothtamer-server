from datetime import datetime as dt
from datetime import timezone as tz
from flask_login import UserMixin

from slothtamer.lib.database import db


class User(db.Model, UserMixin):
    """ User Model """

    __tablename__ = 'users'
    __table_args__ = {'sqlite_autoincrement': True}

    id = db.Column(db.Integer, primary_key=True)
    api_key = db.Column(db.String(64), index=True)
    created = db.Column(db.DateTime, default=dt.now(tz.utc))
    updated = db.Column(db.DateTime, default=dt.now(tz.utc), onupdate=dt.now(tz.utc))


    def __repr__(self):
        return "<User(id='%s', api_key='%s')>" % (self.id, self.api_key)


    def to_dict(self):
        return dict(id=self.id, api_key=self.api_key, created=self.created.isoformat(),
                    updated=self.updated.isoformat())
