from sqlalchemy import Column, String, Integer, Text

from app.models.base import BaseModel


class ResultModel(BaseModel):
    __tablename__ = "results"
    id = Column("id", Integer, primary_key=True)
    task_id = Column("task_id", Integer)
    url_id = Column("url_id", Integer)  # 关联URL模型的ID
    risk = Column("risk", Integer)
    url = Column("url", String(500))
    request = Column("request", Text)
    response = Column("response", Text)
    vul_type = Column("vul_type", String(100))
    cve_id = Column("cve_id", String(50))  # CVE编号
    description = Column("description", Text)
    severity = Column("severity", Integer)
    impact_scope = Column("impact_scope", Text)  # 漏洞影响范围
    proof = Column("proof", Text)
    solution = Column("solution", Text)
    fix_status = Column("fix_status", Integer, default=0)  # 修复状态，0未修复，1已修复
    reproduce_steps = Column("reproduce_steps", Text)  # 漏洞复现步骤
    discover_time = Column("discover_time", Integer)
    vulnerability_id = Column("vulnerability_id", Integer)  # 关联漏洞库表的ID
