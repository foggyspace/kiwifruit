from contextlib import contextmanager
from datetime import datetime

from flask_sqlalchemy import SQLAlchemy as _SQLAlchemy, BaseQuery
from sqlalchemy import Integer, Column, SmallInteger, orm


class SQLAlchemy(_SQLAlchemy):
    @contextmanager
    def auto_commit(self):
        try:
            yield
            self.session.commit()
        except Exception as e:
            db.session.rollback()
            raise e


class Query(BaseQuery):
    def filter_by(self, **kwargs):
        if 'status' not in kwargs.keys():
            kwargs['status'] = 1
        return super(Query, self).filter_by(**kwargs)


db = SQLAlchemy()


class BaseModel(db.Model):
    __abstract__ = True
    created_time = Column(Integer)
    status = Column(SmallInteger, default=1)

    def __init__(self) -> None:
        self.created_time = int(datetime.now().timestamp())

    def __getitem__(self, item):
        return getattr(self, item)

    @property
    def created_datetime(self):
        if self.created_time:
            return datetime.fromtimestamp(self.created_time)
        return None

    def set_attrs(self, attrs_dicts):
        for k, v in attrs_dicts.items():
            if hasattr(self, k) and k != 'id':
                setattr(self, k, v)

    def delete(self):
        self.status = 0

