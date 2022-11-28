from app.extensions import db

class Task(db.Model):
    __tablename__ = 'task'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    status = db.Column(db.Integer)
    start_url = db.Column()
    base = db.Column()
    url_count = db.Column()
    progress = db.Column()
    spider_flag = db.Column()
    robots_parsed = db.Column()
    sitemap_parsed = db.Column()
    reachable = db.Column()
    start_time = db.Column()
    end_time = db.Column()


class Url(db.Model):
    __tablename__ = 'url'
    id = db.Column(db.Integer, primary_key=True)
    task_id = db.Column()
    url = db.Column()
    method = db.Column()
    params = db.Column()
    referer = db.Column()
    start_time = db.Column()
    end_time = db.Column()


class Result(db.Model):
    __tablename__ = 'result'
    id = db.Column(db.Integer, primary_key=True)
    task_id = db.Column()
    rule_id = db.Column()
    risk = db.Column(1) # 1 low 2 middle 3 high
    url = db.Column()
    detail = db.Column()
    request = db.Column()
    response = db.Column()


class Rule(db.Model):
    __tablename__ = 'rule'
    id = db.Column(db.Integer, primary_key=True)
    rule_id = db.Column()
    rule_name = db.Column()
    run_type = db.Column()
    risk = db.Column()
    priority = db.Column()
    file_name = db.Column()
    category_id = db.Column()
    description = db.Column()
    solution = db.Column()

