import os
import sys

from lib.core.crawler import CrawlEngine
from lib.core.logs import ERROR, DEBUG
from lib.core.data import conf as config, Url, ObjectDict
from lib.core.settings import PLUGIN_RULES, RULE_TABLE, RUN_URL_DEFAULT_FUN, RUN_DOMAIN_DEFAULT_FUN ,\
                           URL_TABLE, RESULT_TABLE
from lib.db import db

import gevent
from gevent import pool, spawn, joinall


def attr_from_script(scriptname, attr):
    try:
        path = "%s.%s" %(PLUGIN_RULES, scriptname)
        __import__(path)
        module = sys.modules[path]
        try:
            attr = getattr(module, attr)
            return attr
        except AttributeError:
            ERROR("AttributeError,path:%s has no %s attribute" % (path, attr))
    except ImportError:
        ERROR("ImportError,path:%s" % scriptname)   


class ScanEngine(object):
    def __init__(self):
        self.pool = pool.Pool(10)
        self.task_id = config.taskid
        self.goon = config.goon  #continue run
        self.ruleattr = ObjectDict()
        self.host = config.host
        self.hostdomain = "%s://%s" % (config.scheme, config.host)
        self.domain = config.domain
        self.finished_progress = config.finished_progress
        self.initRule()

    def initRule(self):
        self.ruleattr.domain = self.domain
        self.ruleattr.site_type = config.site_type

    def run(self):
        DEBUG("ScanEngine start")
        joinall([
            spawn(self.scheduleUrl),
            spawn(self.scheduleDomain)
            ])
        self.pool.join()
        self.update_progress('END')
        DEBUG("ScanEngine end")

    def scheduleUrl(self):
        """
        run_type为1,脚本需定义run_url方法
        """
        DEBUG("scheduleUrl start")
        sql = "SELECT `rule_id`,`risk`,`file_name` FROM `%s` WHERE `run_type` = 1 ORDER BY  `priority`" % RULE_TABLE
        rules = [(str(rule.rule_id), rule.file_name, rule.risk) for rule in db.iter(sql) if str(rule.rule_id) not in self.finished_progress]

        if not config.spider_finish:
            CrawlEngine.start()

        sql = "SELECT `url`,`method`,`params`,`referer` FROM %s WHERE `task_id`=%s" % (URL_TABLE, self.task_id)

        reqs = [Url(url.url, url.method, url.params, url.referer) for url in db.iter(sql)]

        for rule_id, filename, risk in rules:
            run_url = attr_from_script(filename, RUN_URL_DEFAULT_FUN)
            if run_url:
                DEBUG("rule_id:%s filename:%s run_url start" % (rule_id, filename))
                for req in reqs:
                    self.pool.spawn(self.runUrl, rule_id, run_url, req, filename, risk)
                    gevent.sleep(0)
                DEBUG("rule_id:%s filename:%s run_url end" % (rule_id, filename))
        DEBUG("scheduleUrl end")

    def runUrl(self, rule_id, run_url, req, filename, risk):
        result = None
        try:
            self.update_progress(rule_id)
            result = run_url(req, self.ruleattr)
        except Exception:
            ERROR("rule_id:%s,scriptname:%s exception" %(rule_id, filename))

        if result is not None:
            try:
                self.analyse_result(rule_id, risk, result, req.url)
            except Exception:
                ERROR('analyse_result exception,rule_id:%s' % rule_id)

    def scheduleDomain(self):
        DEBUG("scheduleDomain start")
        sql = "SELECT `rule_id`,`risk`,`file_name` FROM `%s` WHERE `run_type` = 2 ORDER BY  `priority`" % RULE_TABLE
        domainRule = [ (str(rule.rule_id), rule.file_name, rule.risk) for rule in db.iter(sql) if str(rule.rule_id) not in self.finished_progress]
        for rule_id, filename, risk in domainRule:
            run_domain = attr_from_script(filename, RUN_DOMAIN_DEFAULT_FUN)
            if run_domain:
                DEBUG("rule_id:%s filename:%s run_domain start" % (rule_id, filename))
                self.pool.spawn(self.runDomain, rule_id, run_domain, filename, risk)
                gevent.sleep(0)
                DEBUG("rule_id:%s filename:%s run_domain end" % (rule_id, filename))
        DEBUG("scheduleDomain end")

    def runDomain(self, rule_id, run_domain, filename, risk):
        result = None
        try:
            self.update_progress(rule_id)
            result = run_domain(self.ruleattr)
        except Exception:
            ERROR("rule_id:%s,scriptname:%s exception" %(rule_id, filename))

        if result is not None:
            try:
                self.analyse_result(rule_id, risk, result, self.domain)
            except Exception:
                ERROR('analyse_result exception,rule_id:%s' % rule_id)

    def analyse_result(self, rule_id, risk, result, url):
        response = result.response
        details = result.details
        risk = {'low':1, 'middle':2, 'high':3}.get(risk, 1)
        details = "\r\n".join(details) if isinstance(details,(list,tuple)) else details
        requrl = response.request.url
        request = self.generateRequest(response.request,requrl)
        response = self.generateResponse(response)
        sql = "INSERT INTO %s" % RESULT_TABLE
        data = [ attr.encode('utf-8') for attr in (self.task_id,rule_id,str(risk),requrl,details,request,response) ]
        sql += "(`task_id`,`rule_id`,`risk`,`url`,`detail`,`request`,`response`) VALUES(%s,%s,%s,%s,%s,%s,%s)"
        db.execute(sql,*data)

    def generateRequest(self, request, url):
        req = []
        path = url.partition(self.hostdomain)[-1]
        method = request.method
        req.append("%s %s HTTP/1.0" % (method, path))
        req.append("Host: %s" % self.host)
        for k, v in request.headers.iteritems():
            req.append("%s: %s" % (k, v))
        if method == "POST":
            req.append("")
            if request.body is not None:
                req.append(request.body)
        return "\r\n".join(req)

    def generateResponse(self,response):
        res = []
        res.append("HTTP/1.0 %s %s" % (response.status_code, response.reason))
        for k, v in response.headers.iteritems():
            res.append("%s: %s" % (k, v))
        return "\r\n".join(res)

    def update_progress(self, rule_id):
        try:
            sql = "SELECT `progress` FROM task WHERE id=%s" % self.task_id
            progress = db.get(sql).progress
            if rule_id not in progress.split('|'):
                progress += '|%s' % rule_id
                sql = "UPDATE task SET `progress`='%s' WHERE id=%s" % (progress, self.task_id)
                db.execute(sql)
        except Exception:
            ERROR("update_progress exception")


def run():
    engine = ScanEngine()
    engine.run()

