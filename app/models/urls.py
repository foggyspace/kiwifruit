from sqlalchemy import Column, String, Integer
from app.models.base import BaseModel


class URLModel(BaseModel):
    __tablename__ = "urls"
    id = Column("id", Integer, primary_key=True)
    task_id = Column("task_id", Integer)
    method = Column("method", String(30))
    params = Column("params", String(128), blank=True)
    referer = Column("referer", String(255), blank=True)
    start_time = Column("start_time", Integer)
    end_time = Column("end_time", Integer)


