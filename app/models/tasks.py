from sqlalchemy import Column, Integer, String, Text
from app.models.base import Base


# 任务
class VulnTasks(Base):
    __tablename__ = 'vuln_tasks'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column('task_name', String(50))
    target = Column('target', String(128))
    task_id = Column('task_id', Integer)
    task_status = Column('task_status', Integer)

    def __repr__(self):
        return '<VulnTasks : %s>' % self.name

    def update_task_status(self, status, job_id):
        pass

    def get_task_status(self, job_id):
        pass

    def get_all_tasks(self):
        pass


# URL
class Urls(Base):
    __tablename__ = 'urls'
    id = Column(Integer, primary_key=True, autoincrement=True)
    url = Column('url', String(200))
    method = Column('method', String(32))
    params = Column('params', String(50))
    task_id = Column('task_id', Integer)

    def __repr__(self):
        return '<Urls : %s>' % self.url


# 漏洞库表
class Vulns(Base):
    __tablename__ = 'vulns'
    id = Column(Integer, primary_key=True, autoincrement=True)
    vuln_id = Column('vuln_id', Integer, unique=True)
    vuln_name = Column('vuln_name', String(100), unique=True)
    vuln_rank = Column('vuln_rank', Integer, default=1)
    vuln_refrencens = Column('vuln_refrencens', String(128))
    vuln_description = Column('vuln_description', Text)
    vuln_solution = Column('vuln_solution', Text)

    def __repr__(self):
        return '<Vulns : %s>' % self.vuln_name


# 漏扫结果
class VulnResult(Base):
    __tablename__ = 'vuln_result'
    id = Column(Integer, primary_key=True, autoincrement=True)
    vuln_name = Column('vuln_name', String(50))
    vuln_params = Column('vuln_params', String(128))
    vuln_payload = Column('vuln_payload', String(200))
    vuln_url = Column('vuln_url', String(255))
    vuln_request_header = Column('vuln_request_header', Text)
    vuln_response_header = Column('vuln_response_header', Text)
    vuln_response_content = Column('vuln_response_content', Text)

    def __repr__(self):
        return '<VulnResult : %s>' % self.vuln_url

