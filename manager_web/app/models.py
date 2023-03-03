from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


class Task(db.Model):
    __tablename__ = "task"
    name = db.Column(db.String(200))
    status = db.Column(db.Integer)
    start_url = db.Column(db.String(255))
    base = db.Column(db.String(40))
    url_count = db.Column(db.Integer)
    progress = db.Column(db.Text)
    spider_flag = db.Column(db.Integer, default=1)
    robots_parsed = db.Column(db.Boolean, default=False)
    sitemap_parsed = db.Column(db.Boolean, default=False)
    reachable = db.Column(db.Boolean, default=True)
    start_time = db.Column(db.DateTime)
    end_time = db.Column(db.DateTime)
   

class Url(db.Model):
    __tablename__ = "url"

    task_id = db.Column(db.Integer)
    url = db.Column(db.String(255))
    method = db.Column(db.String(5))
    params = db.Column(db.String(200))
    referer = db.Column(db.String(200))
    start_time = db.Column(db.DateTime)
    end_time = db.Column(db.DateTime)


class Result(db.Model):
    __tablename__ = "result"

    task_id = db.Column(db.Integer)
    rule_id = db.Column(db.Integer)
    risk = db.Column(db.Integer, default=1) # 1 low 2 middle 3 high
    url = db.Column(db.String(255))
    detail = db.Column(db.Text)
    request = db.Column(db.Text)
    response = db.Column(db.Text)


class Rule(db.Model):
    __tablename__ = "rule"

    rule_id = db.Column(db.Integer)
    rule_name = db.Column(db.String(128))
    run_type = db.Column(db.Integer, default=1)
    risk = db.Column(db.String)
    priority = db.Column(db.Integer, default=1)
    file_name = db.Column(db.String(128))
    category_id = db.Column(db.Integer)
    description = db.Column(db.Text)
    solution = db.Column(db.Text)

