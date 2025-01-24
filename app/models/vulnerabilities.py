from sqlalchemy import Column, String, Integer, Text, Float
from app.models.base import BaseModel


class VulnerabilityModel(BaseModel):
    __tablename__ = "vulnerabilities"
    id = Column("id", Integer, primary_key=True)
    name = Column("name", String(200))  # 漏洞名称
    vul_type = Column("vul_type", String(100))  # 漏洞类型
    cve_id = Column("cve_id", String(50))  # CVE编号
    cvss_score = Column("cvss_score", Float)  # CVSS评分
    description = Column("description", Text)  # 漏洞描述
    impact_scope = Column("impact_scope", Text)  # 影响范围
    solution = Column("solution", Text)  # 修复方案
    reference = Column("reference", Text)  # 参考链接
    reproduce_steps = Column("reproduce_steps", Text)  # 复现步骤
    severity = Column("severity", Integer)  # 危险等级
    created_by = Column("created_by", Integer)  # 创建者ID
    updated_by = Column("updated_by", Integer)  # 更新者ID
    updated_time = Column("updated_time", Integer)  # 更新时间