import copy
import json
from datetime import datetime
from urllib.parse import urlsplit, urlparse

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext, loader
from django.contrib.auth.decorators import login_required
from django.utils.html import escape

from icepie.app_site.models import Task, Result, Rule, Url
from icepie.app_site.utils import json_error, json_success, enum, get_domain, send_request

TASK = enum("WAIT", "RUNNING", "STOP", "FINISH")
SPIDER = enum("WAIT", "RUNNING", "STOP", "FINISH")
RISK = enum("LOW", "MIDDLE", "HIGH", start=1)


def task_percent(tasks):
    for task in tasks:
        h_c = Result.objects.filter(task_id=task.id, risk=RISK.HIGH).count()
        m_c = Result.objects.filter(task_id=task.id, risk=RISK.MIDDLE).count()
        l_c = Result.objects.filter(task_id=task.id, risk=RISK.LOW).count()
        c = h_c + m_c + l_c
        if c == 0:
            s_c = 0
            s_p = 100
            c = 1
        else:
            s_c = 0
            s_p = 0

        h_p = int(float(h_c) / c * 100)
        m_p = int(float(m_c) / c * 100)
        l_p = (100 - h_p - m_p) if l_c > 0 else 0
        sum_p = h_p + m_p + l_p
        if sum_p != 100 and sum_p != 0:
            diff = 100 - sum_p
            if h_p != 0:
                h_p += diff
            elif m_p != 0:
                m_p += diff
            else:
                l_p += diff

        for attr in ("h_c", "m_c", "l_c", "s_c", "h_p", "m_p", "l_p", "s_p"):
            setattr(task, attr, vars().get(attr, 0))
    return tasks


def index(request):
    if request.user.is_authenticated():
        tasks = Task.objects.order_by("-id")
        tasks = task_percent(tasks)
        return render(request, "home/home.html", locals())
    else:
        return HttpResponseRedirect("/login/")


@login_required(login_url="/login/")
def task(request):
    action = request.POST.get("action", "error")
    func = "do_" + action
    f = getattr(DoTask, func, DoTask.do_error)
    return f(request)


class DoTask(object):
    MODULE_NAME = "SCAN_MODULE"

    @classmethod
    def do_create(cls, request):
        task_name = request.POST.get("task_name")
        task_start_url = request.POST.get("task_start_url")
        task_base = request.POST.get("task_base")
        task_url_count = request.POST.get("task_url_count")
        task_status = TASK.WAIT
        task = Task(name=task_name, status=task_status, start_url=task_start_url, base=task_base, url_count=task_url_count, spider_flag=SPIDER.WAIT)
        task.save()
        task.s_c = 0
        task.s_p = 100
        return render(request, "home/task_template.html", locals())

    @classmethod
    def do_refresh(cls, request):
        task = Task.objects.order_by("-id")
        task = task_percent(task)
        return render(request, "home/task_template.html", locals())

    @classmethod
    def do_get(cls, request):
        pass
