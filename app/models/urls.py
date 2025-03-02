from sqlalchemy import Column, String, Integer, Text
from app.models.base import BaseModel


class URLModel(BaseModel):
    __tablename__ = "urls"
    id = Column("id", Integer, primary_key=True)
    task_id = Column("task_id", Integer)
    url = Column("url", String(500))
    method = Column("method", String(30))
    params = Column("params", String(128), nullable=True)
    post_data = Column("post_data", Text, nullable=True)
    referer = Column("referer", String(255), nullable=True)
    request_headers = Column("request_headers", Text, nullable=True)
    response_headers = Column("response_headers", Text, nullable=True)
    response_status = Column("response_status", Integer)
    content_type = Column("content_type", String(100), nullable=True)
    start_time = Column("start_time", Integer)
    end_time = Column("end_time", Integer)


