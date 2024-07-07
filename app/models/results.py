from sqlalchemy import Column, String, Integer

from app.models.base import BaseModel


class ResultModel(BaseModel):
    __tablename__ = "results"
    id = Column("id", Integer, primary_key=True)
    task_id = Column("task_id", Integer)
    risk = Column("risk", Integer)
    url = Column("url", String(500))
    request = Column("request", String(500))
    response = Column("response", String(500))
