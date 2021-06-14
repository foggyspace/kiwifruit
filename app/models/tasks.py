from datetime import datetime
from app.extensions import db


class Tasks(db.Model):
    __tablename__ = 'tasks'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column('任务名称', db.String(50), nullable=False, unique=True)
    target = db.Column('检测目标', db.String(255), nullable=False)
    status = db.Column('任务状态', db.Integer(), default=0)
    task_id = db.Column('任务ID', db.Integer(), unique=True)
    start_time = db.Column('开始时间', db.DateTime, nullable=False, default=datetime.utcnow)
    end_tiem = db.Column('结束时间', db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return '<task name : %s task status %s>' % self.name, self.status


class Urls(db.Model):
    __tablename__ = 'urls'
    id = db.Column(db.Integer(), primary_key=True)
    task_id = db.Column('任务ID', db.Integer(), nullable=False)
    url = db.Column('url链接', db.String(400))
    method = db.Column('请求方法', db.String(10))
    params = db.Column('请求参数', db.String(255), nullable=True)
    referer = db.Column('请求源地址', db.String(400))
    start_time = db.Column('开始时间', db.DateTime, default=datetime.utcnow)
    end_time = db.Column('结束时间', db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<task id : %d>' % self.task_id

