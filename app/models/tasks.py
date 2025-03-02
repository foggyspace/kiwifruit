from sqlalchemy import Column, Integer, String
from app.models.base import BaseModel


class Task(BaseModel):
    __tablename__ = "tasks"
    id = Column("id", Integer, primary_key=True)
    task_id = Column("task_id", String(255))
    name = Column("name", String(128))
    status = Column("status", Integer)
    start_url = Column("start_url", String(255))
    url_count = Column("url_count", Integer)
    start_time = Column("start_time", String(128))
    end_time = Column("end_time", String(128))


    def update_status(self, status: int, task_id: str) -> None:
        '''更新任务状态'''
        ...

    def create_task(self, **kwargs) -> None:
        '''创建任务'''
        ...
