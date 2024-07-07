from sqlalchemy import Column, Integer, String
from app.models.base import BaseModel


class Task(BaseModel):
    __tablename__ = "tasks"
    id = Column("id", primary_key=True)
    name = Column("name", String(128))
    status = Column("status", Integer)
    start_url = Column("start_url", String(255))


    def update_status(self, status: int) -> None:
        ...

    def create_task(self, **kwargs) -> None:
        ...
