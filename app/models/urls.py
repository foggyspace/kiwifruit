from sqlalchemy import Column, String, Integer, Text
from app.models.base import BaseModel


class URLModel(BaseModel):
    __tablename__ = "urls"
    id = Column("id", Integer, primary_key=True)
    task_id = Column("task_id", Integer)
    url = Column("url", String(500))
    method = Column("method", String(30))
    params = Column("params", String(128), blank=True)
    post_data = Column("post_data", Text, blank=True)
    referer = Column("referer", String(255), blank=True)
    request_headers = Column("request_headers", Text, blank=True)
    response_headers = Column("response_headers", Text, blank=True)
    response_status = Column("response_status", Integer)
    content_type = Column("content_type", String(100), blank=True)
    start_time = Column("start_time", Integer)
    end_time = Column("end_time", Integer)


