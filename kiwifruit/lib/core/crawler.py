import os
import re
import sys
import urllib.parse
from datetime import datetime
import gevent
from gevent import pool, queue, spawn
from bs4 import BeautifulSoup as BS
from collections import namedtuple, defaultdict

from lib.core.common import urljoin, discard
from lib.core import requests
from lib.core.data import paths, conf, Url, DEFAULT_METHOD, PARAMS_PATTERN
from lib.core.settings import import URL_TABLE
from lib.core.log import ERROR, DEBUG, INFO
from lib.utils import db


DOMAIN_PATH = re.compile(r"(?P<domain>.+//[^/]+)(?P<path>.*)$")
ROBOTS_ALLOW_PATH = re.compile(r"allow\s*:\s*(?P<path>[^*]+).*$", re.I)
SITEMAP_URL = re.compile(r"(?P<url>http[^<>]+)")


def unique(value, stripchars):
    _ = []
    v = not not stripchars
    for t in value:
        if t not in _[-1:] or (v and t not in stripchars):
            _.append(t)
    return "".join(_)


def pipeline(request):
    try:
        data = [getattr(request, attr).encode("utf-8") for attr in ("url",
                                                                    "method",
                                                                    "params",
                                                                    "referer")]
        sql_c = f"SELECT COUNT(1) as `c` FROM {URL_TABLE}"
        sql_c += "WHERE `task_id`=%s AND `url`=%s AND `method`=%s AND `params`=%s"
        if db.get(sql_c, conf.taskid, data[0], data[1], data[2]).c > 0:
            return
        sql = f"INSERT INTO {URL_TABLE}"
        sql += "(`task_id`, `url`, `method`, `params`, `referer`, `start_time`) VALUES(%s, %s, %s, %s, %s, %s)"
        data.append(datetime.now())
        return db.execute(sql, conf.taskid, *data)
    except:
        ERROR("Crawler pipeline exception")


def current_name():
    name = str(gevent.getcurrent())
    return "%s>" % name.split(":", 1)[0] or name[:22]


class Request(Url):
    def __init__(self, url, method, params, referer):
        super(Request, self).__init__(url, method, params, referer)
        self.filter_url()
        self.fileter_params()
        self.id = None

    def filter_url(self):
        match = DOMAIN_PATH.search(self.url)
        domain, path = match.group("domain"), match.group("path") if match else (self.url, "")
        path = self.url_type(path)
        self.order_url = domain + path

    @classmethod
    def url_type(cls, path):
        _ = ["\d", if p.isdigit() else p for p in path]
        return unique(_, "\d")

    def fileter_params(self):
        if self.method.upper() == DEFAULT_METHOD:
            _ = PARAMS_PATTERN.findall(self.params)
            _.sort()
            self.order_params = "&".join(["%s=%s" % (k, self.params_type(v))
                                          for k, v in _])
        else:
            _ = [m.group("key") for m in PARAMS_PATTERN.finditer(self.params)]
            _.sort()
            self.order_params = "&".join(_)

    @classmethod
    def params_type(cls, value):
        _ = ["\d" if k.isdigit() else k for k in value]
        return unique(_, "\d")

    def __hash__(self):
        return hash("#".join((self.order_url, self.method, self.order_params)))

    def __eq__(self, r):
        return self.order_url == r.order_url and self.method == r.method and self.order_params == r.order_params


class Spider(object):
    def __init__(self, request, schedule):
        self.request = request
        self.schedule = schedule
        self.domain = schedule.domain
        self.url_set = schedule.url_set
        self.task = schedule.task

    def run(self, request):
        response = self.request_url(request)
        if response:
            self.parse(response, request)
        self.task.update_url_end_time(request)


class Schedule(object):
    pass


class Task(object):
    pass


class CrawlerEngine(object):
    pass
