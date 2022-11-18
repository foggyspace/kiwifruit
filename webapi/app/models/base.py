from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer
from datetime import datetime

from app.extensions import db


__all__ = ['db', 'Base']


class Base(db.Model):
    __abstract__ = True
    create_time = Column('create_time', Integer)
    status = Column('status', default=1)

    def __init__(self):
        self.create_time = int(datetime.now().timestamp())

    @property
    def create_datetime(self):
        if self.create_time:
            return datetime.fromtimestamp(self.create_time)
        else:
            return None

    def delete(self):
        self.status = 0

    def set_attrs(self, **options):
        for key, value in options.items():
            if hasattr(self, key) and key != 'id':
                setattr(self, key, value)

