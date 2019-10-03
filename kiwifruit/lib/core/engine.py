import sys

from kiwifruit.lib.core.crawler import CrawlEngine
from kiwifruit.lib.core.log import ERROR, DEBUG
from kiwifruit.lib.core.data import conf, Url, ObjectDict
from kiwifruit.lib.core.config import URL_TABLE, RESULT_TABLE, SCRIPTS_NAME, RUN_DOMAIN_DEFAULT_FUN, RUN_URL_DEFAULT_FUN, RULE_TABLE
from kiwifruit.lib.common import db

import gevent
from gevent import pool, spawn, joinall


def attr_from_script(script_name, attr):
    try:
        path = "%s.%s" % (SCRIPTS_NAME, script_name)
        __import__(path)
        module = sys.modules[path]
        try:
            attr = getattr(module, attr)
            return attr
        except AttributeError:
            ERROR("[-] AttributeError path : %s has no %s attribute" % (path, attr))
    except ImportError:
        ERROR("[-] ImportError path : %s" % path)


class ScanEngine(object):
    def __init__(self):
        self.pool = pool.Pool(10)
        self.task_id = conf.taskid
        self.goon = conf.goon
        self.rule_attr = ObjectDict()
        self.host = conf.host
        self.host_domain = "%s://%s" % (conf.scheme, conf.host)
        self.domain = conf.domain
        self.finished_progress = conf.finished_progress
        self.init_rule()

    def init_rule(self):
        self.rule_attr.domain = self.domain
        self.rule_attr.site_type = conf.site_type

    def run(self):
        DEBUG("[*] Scan Engine start.")
        joinall([
            spawn(self.schedule_url),
            spawn(self.schedule_domain)
        ])

        self.pool.join()
        self.update_progress("END")
        DEBUG("Scan Engine END.")

    def schedule_url(self):
        DEBUG("[*] schedule url start")
        sql = "SELECT `rule_id`, `risk`, `file_name` FROM `%s` WHERE `rule_type` = 1 ORDER BY `priority`" % RULE_TABLE
        rules = [(str(rule.rule_id), rule.file_name, rule.risk) for rule in db.iter(sql) if str(rule.rule_id) not in self.finished_progress]

        if not conf.spider_finish:
            CrawlEngine.start()

        sql = "SELECT `url`, `method`, `params`, `referer` FROM %s WHERE `task_id`=%s" % (URL_TABLE, self.task_id)

        reqs = [Url(url.url, url.method, url.params, url.referer) for url in db.iter(sql)]

        for rule_id, filename, risk in rules:
            run_url = attr_from_script(filename, RUN_URL_DEFAULT_FUN)
            if run_url:
                DEBUG("[*] rule id : %s filename : %s run url start" % (rule_id, filename))
                for req in reqs:
                    self.pool.spawn(self.run_url, rule_id, run_url, req, filename, risk)
                    gevent.sleep(0)
                DEBUG("[*] rule id : %s filename : %s run url end" % (rule_id, filename))
        DEBUG("[*] schedule url end.")

    def run_url(self, rule_id, run_url, req, filename, risk):
        result = None
        try:
            self.update_progress(rule_id)
            result = run_url(req, self.rule_attr)
        except Exception:
            ERROR("[*] rule id : %s script name : %s exception" % (rule_id, filename))

        if result is not None:
            try:
                self.analyse_result(rule_id, risk, result, req.url)
            except Exception:
                ERROR("[*] analyse result exception rule id : %s" % (rule_id, ))

    def schedule_domain(self):
        DEBUG("[*] schedule domain start.")
        sql = "SELECT `rule_id`, `risk`, `file_name` FROM `%s` WHERE `run_type` = 2 ORDER BY `priority`" % RULE_TABLE

        domain_rule = [(str(rule.rule_id), rule.file_name, rule.risk) for rule in db.iter(sql) if str(rule.rule_id) not in self.finished_progress]

        for rule_id, filename, risk in domain_rule:
            run_domain = attr_from_script(filename, RUN_URL_DEFAULT_FUN)
            if run_domain:
                DEBUG("[*] rule_id : %s filename : %s run domain start" % (rule_id, filename))
                self.pool.spawn(self.run_domain, rule_id, run_domain, filename, risk)
                gevent.sleep(0)
                DEBUG("[*] rule_id : %s filename : %s run domain end" % (rule_id, filename))
        DEBUG("[*] schedule domain end")

    def run_domain(self, rule_id, run_domain, filename, risk):
        result = None
        try:
            self.update_progress(rule_id)
            result = run_domain(self.rule_attr)
        except Exception:
            ERROR("[*] rule_id %s script name : %s exception " % (rule_id, filename))

        if result is not None:
            try:
                self.analyse_result(rule_id, risk, result, self.domain)
            except Exception:
                ERROR("[*] analyse result exception rule id : %s" % rule_id)

    def analyse_result(self, rule_id, risk ,result, url):
        response = result.response
        details = result.details
        risk = {"low": 1, "middle": 2, "high": 3}.get(risk, 1)
        details = "\r\n".join(details) if isinstance(details, (list, tuple)) else details
        req_url = response.request.url
        request = self.generate_request(response.request.url)
        response = self.generate_response(response)
        sql = "INSERT INTO %s" % RESULT_TABLE
        data = [attr.encode("utf-8") for attr in (self.task_id, rule_id, str(risk), req_url, details, request, response)]
        sql += "(`task_id`, `rule_id`, `risk`, `url`, `detail`, `request`, `response`) VALUES(%s, %s, %s, %s, %s, %s, %s)"
        db.execute(sql, *data)

    def generate_request(self, request, url):
        req = []
        path = url.partition(self.host_domain)[-1]
        method = request.method
        req.append("%s %s HTTP/1.0" % (method, path))
        req.append("Host: %s" % self.host)
        for k, v in request.headers.items():
            req.append("%s: %s" % (k, v))
        if method == "POST":
            req.append("")
            if request.body is not None:
                req.append(request.body)
        return "\r\n".join(req)

    def generate_response(self, response):
        res = []
        res.append("HTTP/1.0 %s %s" % (response.status_code, response.reason))
        for k, v in response.headers.items():
            res.append("%s: %s" % (k, v))
        return "\r\n".join(res)

    def update_progress(self, rule_id):
        try:
            sql = "SELECT `progress` FROM task WHERE id=%s" % (self.task_id, )
            progress = db.get(sql).progress
            if rule_id not in progress.split("|"):
                progress += "|%s" % rule_id
                sql = "UPDATE task SET `progress`='%s' WHERE id=%s" % (progress, self.task_id)
                db.execute(sql)
        except Exception:
            ERROR("[*] update progress exception")


def run():
    engine = ScanEngine()
    engine.run()
