from app.extensions import db


class VulnsResult(db.Model):
    __tablename__ = 'vulns_result'
    id = db.Column(db.Integer(), primary_key=True)
    task_id = db.Column('任务ID', db.Integer())
    vuln_url = db.Column('漏洞链接', db.String(400), nullable=False)
    requests = db.Column('请求头部', db.Text)
    response = db.Column('响应内容', db.Text)

    def __repr__(self):
        return '<task id : %d>' % self.task_id

    def get_vuln_detail(self, id):
        data = VulnsResult.query.filter_by(id=id).first()
        return data

    def get_vuln_all_by_task_id(self, task_id):
        data = VulnsResult.query.filter_by(task_id).all()
        return data
