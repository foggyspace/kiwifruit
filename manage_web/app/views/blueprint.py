from flask import render_template, request, redirect

from . import vuln_bp
from app.enums import RiskLevelEnum, SpiderStausEnum, TaskStatusEnum
from app.models import Result, Rule, Task, Url, db


def task_percent(tasks):
    for task in tasks:
        h_c = Result.query.filter_by(task_id=task.id, risk=RiskLevelEnum.HIGH).count()
        m_c = Result.query.filter_by(task_id=task.id, risk=RiskLevelEnum.MIDDLE).count()
        l_c = Result.query.filter_by(task_id=task.id, risk=RiskLevelEnum.LOW).count()

        c = h_c + m_c + l_c
        if c == 0:
            s_c = 0
            s_p = 100
            c = 1
        else:
            s_c = 0
            s_p = 0

        h_p = int(float(h_c)/c*100)
        m_p = int(float(m_c)/c*100)
        l_p = (100 - h_p - m_p) if l_c > 0 else 0
        sum_p = h_p + m_p + l_p
        if  sum_p != 100 and sum_p != 0: ##弥补可能和不是100%误差
            diff = 100 - sum_p
            if h_p != 0:
                h_p += diff
            elif m_p != 0:
                m_p += diff
            else:
                l_p += diff
                
        for attr in ('h_c','m_c','l_c','s_c','h_p','m_p','l_p','s_p'):
            setattr(task, attr, vars().get(attr,0))
    return tasks



@vuln_bp.route("/home")
def home():
    tasks = db.session.query(Task).all()
    #tasks = Task.query.order_by("id desc")
    tasks = task_percent(tasks=tasks)
    return render_template("home/home.html", tasks=[tasks])


@vuln_bp.route("/add", methods=["GET", "POST"])
def add():
    if request.method == "POST":
        task_name = request.form.get("task_name")
        task_starturl = request.form.get("task_starturl")
        task_base = request.form.get("task_base")
        task_urlcount = request.form.get("task_urlcount")
        #task_status = TaskStatusEnum.WAIT
        task_status = 0

        task = Task(name=task_name, status=task_status, start_url=task_starturl, base=task_base,
                url_count=task_urlcount, spider_flag=1)
        db.session.add(task)
        db.session.commit()

        return render_template("home/task_template.html")

