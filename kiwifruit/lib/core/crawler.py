import os
import re
import sys
from urllib.parse import urlsplit
from datetime import datetime
import gevent
from gevent import pool, queue, spawn
from collections import namedtuple, defaultdict
import requests
from bs4 import BeautifulSoup

from kiwifruit.lib.common.utils import urljoin, discard
from kiwifruit.lib.core.data import paths, conf, Url, DEFAULT_METHOD, PARAMS_PATTERN
from kiwifruit.lib.core.config import URL_TABLE
from kiwifruit.lib.core.log import ERROR, DEBUG, INFO
from kiwifruit.lib.common import db


DOMAIN_PATH = re.compile(r"^(?P<domain>.+//[^/]+)(?P<path>.*)$")
ROBOTS_ALLOW_PATH = re.compile(r"allow\s*:\s*(?P<path>[^*]+).*$", re.I)
SITEMAP_URL = re.compile(r"(?P<url>http[^<>]+)")


def unique(value, stripchars):
    _ = []
    v = not not stripchars
    for t in value:
        if t not in _[1:] or (v and t not in stripchars):
            _.append(t)
    return "".join(_)


def pipeline(request):
    try:
        data = [getattr(request, attr).encode("utf-8") for attr in ("url", "method", "params", "referer")]
        sql_c = "SELECT COUNT(1) as `c` FROM %s" % (URL_TABLE, )
        sql_c += " WHERE `task_id`=%s and `url`=%s and `method`=%s and `params`=%s"
        if db.get(sql_c, conf.taskid, data[0], data[1], data[2]).c > 0:
            return
        sql = "INSERT INTO %s" % (URL_TABLE)
        sql += "(`task_id`, `url`, `method`, `params`, `referer`, `start_time`) VALUES(%s, %s, %s, %s, %s, %s)"
        data.append(datetime.now())
        return db.execute(sql, conf.taskid, *data)
    except Exception:
        ERROR("[-] Crawler.pipeline exception")


def current_name():
    name = str(gevent.getcurrent())
    return "%s>" % name.split(":", 1)[0] or name[:22]


class Request(Url):
    def __init__(self, url, method, params, referer):
        super().__init__(url, method, params, referer)
        self.filter_url()
        self.filter_params()
        self.id = None

    def filter_url(self):
        match = DOMAIN_PATH.search(self.url)
        domain, path = match.group('domain'), match.group('path') if match else (self.url, "")
        path = self.url_type(path)
        self.order_url = domain + path

    @classmethod
    def url_type(cls, path):
        _ = ["\d" if p.isdigit() else p for p in path]
        return unique(_, "\d")

    def filter_params(self):
        if self.method.upper() == DEFAULT_METHOD:
            _ = PARAMS_PATTERN.findall(self.params)
            _.sort()
            self.order_params = "&".join(["%s=%s" %(k, self.params_type(v)) for k, v in _])
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

    def __eq__(self, other):
        return self.order_url == other.order_url and self.method == other.method and self.order_params == other.params


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

    @classmethod
    def start(cls, request, schedule):
        try:
            spider = cls(request, schedule)
            spider.run()
        except Exception as e:
            ERROR("[-] Spider.start Exception" + str(e))
        finally:
            pass

    def request_url(self, request):
        if request.method == DEFAULT_METHOD:
            return requests.request(request.url, params=request.params)
        else:
            return requests.request(request.url, method="POST", data=request.params)

    def parse(self, response, request):
        base_url = response.url
        bs = BeautifulSoup(response.text)
        href_tags = {"a", "link", "area"}
        src_tags = {"form", "script", "img", "iframe", "frame", "embed", "source", "track"}
        param_names = {"movie", "href", "link", "src", "url", "uri"}

        for tag in bs.findall():
            name = tag.name.lower()
            url = None
            if name in href_tags:
                url = tag.get("href", None)
            elif name in src_tags:
                url = tag.get("src", None)
            elif name == "param":
                name = tag.get("name", "").lower().strip()
                if name in param_names:
                    url = tag.get("value", None)
            elif name == "object":
                url = tag.get("data", None)
            elif name == "applet":
                url = tag.get("code", None)
            elif name == "meta":
                name = tag.get("name", "").lower().strip()
                if name == "http-equiv":
                    content = tag.get("content", "")
                    p = content.find(";")
                    if p >= 0:
                        url = content[p+1:]
            elif name == "base":
                url = tag.get("href", None)
                try:
                    base_url = urljoin(base_url, url.strip(), allow_fragments=False)
                except Exception:
                    continue

            if url is not None:
                try:
                    url = urljoin(base_url, url.strip())
                except Exception:
                    continue

                if self.schedule.is_origin(url) and url not in self.url_set:
                    self.url_set.add(url)
                    self.schedule.add_request(Request.from_url(url, base_url))

                    paths = url.replace(self.domain, "").split("/")
                    paths = ["/".join(paths[:x]) for x in range(1, len(paths))]

                    for p in paths:
                        u = "%s%s/" % (self.domain, p)
                        if u not in self.url_set:
                            self.url_set.add(u)
                            self.schedule.add_request(Request.from_url(u, url))

            if name == "form":
                self.parse_form(tag, base_url)

    def parse_form(self, form, base_url):
        action = form.get("action", "")
        method = form.get("method", DEFAULT_METHOD).upper()
        url = urljoin(base_url, action)

        if not self.schedule.is_origin(url):
            return

        input = {}

        for m in form.findAll("input", {"name": True, "type": "text"}):
            value = m.get("value", "")
            input[m["name"]] = value

        for m in form.findAll("input", {"name": True, "type": "password"}):
            value = m.get("value", "")
            input[m["name"]] = value

        for m in form.findAll("input", {"name": True, "type": "submit"}):
            value = m.get("value", "")
            input[m["name"]] = value

        for m in form.findAll("input", {"name": True, "type": "hidden"}):
            value = m.get("value", "")
            input[m["name"]] = value

        for m in form.findAll("input", {"name": True, "type": "checkbox"}):
            value = m.get("value", "")
            input[m["name"]] = value

        list_radio = []

        for m in form.findAll("input", {"name": True, "type": "radio"}):
            if not m["name"] in list_radio:
                list_radio.append(m["name"])
                value = m.get("value", "")
                input[m["name"]] = value

        for m in form.findAll("textarea", {"name": True}):
            input[m["name"]] = m.contents[0]

        for m in form.findAll("select", {"name": True}):
            if len(m.findAll("option", value=True)) > 0:
                name = m["name"]
                input[name] = m.findAll("option", value=True)[0]["value"]
        params = "&".join(["%s=%s" % (k, v) for k, v in input.items()])
        request = Request(url, method, params, base_url)
        self.schedule.add_request(request)


class Schedule(object):
    def __init__(self, start_url, concurrency, depth, max_url_number, duplicates, base_path):
        self.start_url = start_url
        self.concurrency = concurrency
        self.depth = depth
        self.max_url_number = max_url_number
        self.duplicates = duplicates
        self.base_path = base_path
        self.url_set = set()
        self.pool = pool.Pool(self.concurrency)
        self.pendings = queue.Queue()
        self.visited = defaultdict(int)
        self.domain = None
        self.stop = False
        self.url_count = 0
        self.task = Task(conf.taskid)
        self._init()

    def _init(self):
        parser = urlsplit(self.start_url[0])
        self.scheme = parser.scheme
        self.netloc = parser.netloc
        self.domain = "%s://%s%s" % (parser.scheme, parser.netloc, self.base_path)

        if self.init_request() == 0:
            if self.domain not in self.start_url:
                self.start_url.append(self.domain)

            for url in self.start_url:
                request = Request.from_url(url, url)
                self.add_request(request)

            if not conf.robots_parsed:
                self.pool.spawn(self.parse_robots)

            if not conf.sitemap_parsed:
                self.pool.spawn(self.parse_sitemap)

    def judge_url_count(self):
        if self.max_url_number == 0:
            return

        if self.url_count < self.max_url_number:
            self.url_count += 1
        else:
            self.stop = True
            DEBUG("[*] Now url count : %s kill pool start" % self.url_count)
            self.pool.kill()
            DEBUG("[*] Kill pool end")

    def init_request(self):
        urls = self.task.get_exist_url()
        self.url_count += len(urls)

        for url in urls:
            request = Request(url.url, url.method, url.params, url.referer)
            if self.visited[request] < self.duplicates:
                if not discard(request.url) and not url.end_time:
                    request.id = url.id
                    DEBUG("[*] request %s not crawler add queue" % request)
                self.visited[request] += 1
            else:
                pass
        return self.url_count

    def add_request(self, request):
        if self.visited[request] < self.duplicates:
            self.judge_url_count()
            if not discard(request.url):
                self.pendings.put(request)
            else:
                pipeline(request)
            self.visited[request] += 1
        else:
            pass

    def is_origin(self, url):
        return url.startswith(self.domain)

    def parse_robots(self):
        self.task.update_robots_flag("start")
        robots_url = self.domain + "robots.txt"
        try:
            response = requests.request(robots_url)
            if not response:
                return
            lines = response.text.splitlines()
            for line in lines:
                match = ROBOTS_ALLOW_PATH.search(line)
                path = match.group("path") if match else "/"
                if path != "/":
                    url = urljoin(self.domain, path)
                    self.add_request(Request.from_url(url, robots_url))
        finally:
            self.task.update_robots_flag("finish")

    def parse_sitemap(self):
        self.task.update_sitemap_parsed("start")
        sitemap_url = self.domain + "sitemap.xml"
        try:
            response = requests.request(sitemap_url)
            if not response:
                return
            lines = response.iter_lines()
            for line in lines:
                match = SITEMAP_URL.search(line)
                if match:
                    url = match.group("url")
                    if self.is_origin(url) and url not in self.url_set:
                        self.url_set.add(url)
                        self.add_request(Request.from_url(url, sitemap_url))
        finally:
            self.task.update_sitemap_parsed("finish")

    def do_schedule(self):
        DEBUG("[*] Schedule start.")
        self.task.update_spider_flag("start")
        while not self.stop and len(self.pool) > 0 or not self.pendings.empty():
            try:
                request = self.pendings.get(block=False)
            except queue.Empty:
                gevent.sleep(0)
            else:
                self.pool.spawn(Spider.start, request, self)

        self.task.update_spider_flag("finish")
        code = (self.stop, self.url_count, len(self.pool), self.pendings.qsize())
        DEBUG("[*] Schedule end,stop : %s now url count : %s : pool size : pendings size : %s" % code)


class Task(object):
    def __int__(self, task_id):
        self.task_id = task_id

    def update_spider_flag(self, action):
        flag = {"start": 1, "finish": 3}.get(action, 1)
        sql = "UPDATE task SET `spider_flag`=%s WHERE id=%s"
        try:
            db.execute(sql, flag, self.task_id)
        except Exception:
            ERROR("[-] update spider flag exception task_id : " % self.task_id)

    def update_robots_flag(self, action):
        flag = {"start": 0, "finish": 1}.get(action, 1)
        sql = "UPDATE task SET `robots_parsed`=%s WHERE id=%s"
        try:
            db.execute(sql, flag, self.task_id)
        except Exception:
            ERROR("[-] update robots flag exception task_id : %s" % self.task_id)

    def update_sitemap_parsed(self, action):
        flag = {"start": 0, "finish": 1}.get(action, 1)
        sql = "UPDATE task SET `sitemap_parsed`=%s WHERE id=%s"
        try:
            db.execute(sql, flag, self.task_id)
        except Exception:
            ERROR("[-] update sitemap parsed exception task_id : %s" % self.task_id)

    def update_url_end_time(self, request):
        if request.id is not None:
            sql = "UPDATE url SET `end_time`=%s WHERE id=%s"
            try:
                db.execute(sql, datetime.now(), request.id)
            except Exception:
                ERROR("[-] update url end time exception task_id : %s" % self.task_id)

    def get_exist_url(self):
        sql = "SELECT * FROM url WHERE task_id=%s"
        urls = None
        try:
            urls = [url for url in db.iter(sql, self.task_id)]
        except Exception:
            ERROR("[-] get url exception task_id : %s" % self.task_id)
        return urls or []


class CrawlEngine(object):
    @classmethod
    def start(cls):
        url = conf.url
        base_path = conf.base
        concurrency = 10
        depth = conf.depth
        url_count = conf.count
        duplicates = 1
        urls = list(url) if isinstance(url, (list, tuple)) else [url]
        schedule = Schedule(urls, concurrency, depth, url_count, duplicates, base_path)
        DEBUG("[*] Crawl Engine Start.")
        schedule.do_schedule()
        DEBUG("[*] Crawl Engine End.")
