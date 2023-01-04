import re
from urllib.parse import urlparse
from datetime import datetime
import gevent
from gevent import pool, queue
from bs4 import BeautifulSoup
from collections import defaultdict

from libs.core.tools import urljoin, discard
from libs.core import request
from libs.core.data import config, Url, DEFAULT_METHOD, PARAMS_PATTERN
from libs.core.settings import URL_TABLE
from libs.core.logs import ERROR, DEBUG
from libs.utils import db


DOMAIN_PAHT = re.compile(r"^(?P<domain>.+//[^/]+)(?P<path>.*)$")

ROBOTS_ALLOW_PATH = re.compile(r"allow\s*:\s*(?P<path>[^*]+).*$",re.I)

SITEMAP_URL = re.compile(r"(?P<url>http[^<>]+)")


def unique(value, stripchars):
    _ = []
    v = not not stripchars
    for t in value :
        if t not in _[-1:] or (v and t not in stripchars):
            _.append(t)
    return "".join(_)


def pipeline(request):
    try:
        data = [getattr(request,attr).encode('utf-8') for attr in ('url','method','params','referer')]

        sql_c = "SELECT COUNT(1) as `c` FROM %s" % (URL_TABLE)
        sql_c += " WHERE `task_id`=%s and `url`=%s and `method`=%s and `params`=%s"
        if db.get(sql_c, config.taskid, data[0], data[1], data[2]).c > 0:
            return
        sql = "INSERT INTO %s" % (URL_TABLE)
        sql += "(`task_id`,`url`,`method`,`params`,`referer`,`start_time`) VALUES(%s,%s,%s,%s,%s,%s)"
        data.append(datetime.now())
        return db.execute(sql, config.taskid, *data)
    except Exception:
        ERROR("Crawler.pipeline Exception")
    

def current_name():
    name = str(gevent.getcurrent())
    return "%s>" % name.split(':',1)[0] or name[:22]


class Request(Url):
    def __init__(self, url, method, params, referer):
        super(Request,self).__init__(url,method,params,referer)
        self.filter_url()
        self.filter_params()
        self.id = None

    def filter_url(self):
        """
        handle repeat url,especially url rewrite
        /id/1          /id/2
        /id/1.html     /id/2.html
        """
        match = DOMAIN_PAHT.search(self.url)
        domain, path = match.group('domain'),match.group('path') if match else (self.url,'')
        path = self.url_type(path)
        self.orderUrl = domain + path

    @classmethod
    def url_type(cls,path):
        _ = ['\d' if p.isdigit() else p for p in path ]
        return unique(_,'\d')

    def filter_params(self):
        """
        handle repeat params,base on method
        GET  => id=68(\d) == id = 86(\d)
             attention key and value type
        POST => name=skycrab&age=10 == name=10&age=skycrab
             only attention key
        """
        if self.method.upper() == DEFAULT_METHOD:
            _ = PARAMS_PATTERN.findall(self.params)
            _.sort()
            self.orderParams = "&".join(["%s=%s" %(k,self.params_type(v)) for k,v in _ ])
        else:
            _ = [ m.group('key') for m in PARAMS_PATTERN.finditer(self.params)]
            _.sort()
            self.orderParams = "&".join(_)

    @classmethod
    def params_type(cls,value):
        _ = ['\d' if k.isdigit() else k for k in value ]
        return unique(_,'\d')

    def __hash__(self):
        return hash('#'.join((self.orderUrl,self.method,self.orderParams)))

    def __eq__(self,r):
        return self.orderUrl == r.orderUrl and self.method == r.method and self.orderParams == r.orderParams


class Spider(object):
    def __init__(self,request,schedule):
        self.request = request
        self.schedule = schedule
        self.domain = schedule.domain
        self.urlSet = schedule.urlSet
        self.task = schedule.task
        #DEBUG("pool size:"+str(len(self.schedule.pool)))

    def run(self, request):
        response = self.request_url(request)
        if response:
            self.parse(response,request)
        self.task.update_url_end_time(request)

    @classmethod
    def start(cls,request,schedule):
        try:
            spider = cls(request,schedule)
            spider.run(request)

        except Exception:
            ERROR('Spider.start Exception')
        finally:
            pass

    def request_url(self,request):
        if request.method == DEFAULT_METHOD:
            return request.request(request.url,params=request.params)
        else:
            return request.request(request.url,method="POST",data=request.params)
            
    def parse(self,response,request):
        base_url = response.url
        bs = BeautifulSoup(response.text)
        href_tags = {"a", "link", "area"}
        src_tags = {"form", "script", "img", "iframe", "frame", "embed", "source", "track"}
        param_names = {"movie", "href", "link", "src", "url", "uri"}

        for tag in bs.findAll():
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
                        url = content[ p + 1 : ]
            elif name == "base":
                url = tag.get("href", None)
                try:
                    base_url = urljoin(base_url, url.strip(), allow_fragments = False)
                except Exception:
                    continue
            if url is not None:
                try:
                    url = urljoin(base_url, url.strip())
                except Exception:
                    continue
                if self.schedule.is_origin(url) and url not in self.urlSet:
                    self.urlSet.add(url)
                    self.schedule.add_request(Request.from_url(url,base_url))

                    #add directory
                    paths = url.replace(self.domain,'').split('/')
                    paths =  ['/'.join(paths[:x]) for x in range(1,len(paths))]
                    for p in paths:
                        u = "%s%s/" % (self.domain,p)
                        if u not in self.urlSet:
                            self.urlSet.add(u)
                            self.schedule.add_request(Request.from_url(u,url))
            #handle form 
            if name == "form":
                self.parse_form(tag,base_url)

    def parse_form(self,form,base_url):
        action = form.get('action','')
        method = form.get('method',DEFAULT_METHOD).upper()
        url = urljoin(base_url,action)
        if not self.schedule.is_origin(url):
            return
        input = {}
        #Process <input type="test" name="...
        for m in form.findAll('input',{'name' : True,'type' : 'text'}):
            value = m.get('value','')
            input[m['name']] = value
        #Process <input type="password" name="...
        for m in form.findAll('input',{'name' : True,'type' : 'password'}):
            value = m.get('value','')
            input[m['name']] = value
        #Process <input type="submit" name="...
        for m in form.findAll('input',{'name' : True,'type' : 'submit'}):
            value = m.get('value','')
            input[m['name']] = value
        #Process <input type="hidden" name="...
        for m in form.findAll('input',{'name' : True,'type' : 'hidden'}):
            value = m.get('value','')
            input[m['name']] = value
        #Process <input type="checkbox" name="...
        for m in form.findAll('input',{'name' : True,'type' : 'checkbox'}):
            value = m.get('value','')
            input[m['name']] = value
        #Process <input type="radio" name="...
        listRadio = []
        for m in form.findAll('input',{'name' : True,'type' : 'radio'}):
            if not m['name'] in listRadio:
                listRadio.append(m['name'])
                value = m.get('value','')
                input[m['name']] = value
        #Process <textarea name="...
        for m in form.findAll('textarea',{'name' : True}):
            input[m['name']] = m.contents[0]
        #Process <select name="...
        for m in form.findAll('select',{'name' : True}):
            if len(m.findAll('option',value=True))>0:
                name = m['name']
                input[name] = m.findAll('option',value=True)[0]['value']
        params = '&'.join(["%s=%s" %(k,v) for k,v in input.items()])
        request = Request(url, method, params ,base_url)
        self.schedule.add_request(request)
        

class Schedule(object):
    def __init__(self,start_urls,concurrency,depth,max_url_num,duplicates,basepath):
        self.start_urls = start_urls
        self.concurrency = concurrency
        self.depth = depth
        self.max_url_num = max_url_num
        self.duplicates = duplicates
        self.basepath = basepath
        self.urlSet = set()
        self.pool = pool.Pool(self.concurrency)
        self.pendings = queue.Queue()
        self.visited = defaultdict(int)
        self.domain = None
        self.stop = False
        self.urlcount = 0
        self.task = Task(config.taskid)
        self._init()

    def _init(self):
        parser = urlparse.urlsplit(self.start_urls[0])
        self.scheme = parser.scheme
        self.netloc = parser.netloc
        self.domain = "%s://%s%s" %(parser.scheme,parser.netloc,self.basepath)

        if self.init_request() == 0: #继续扫描，加载未扫描url
            if self.domain not in self.start_urls:
                self.start_urls.append(self.domain)
            for url in self.start_urls:
                request = Request.from_url(url,url)
                self.add_request(request)      

        if not config.robots_parsed:
            self.pool.spawn(self.parse_robots)
        if not config.sitemap_parsed:
            self.pool.spawn(self.parse_sitemap)

    def judge_url_count(self):
        if self.max_url_num == 0:
            return
        if self.urlcount < self.max_url_num:
            self.urlcount += 1
        else:
            self.stop = True
            DEBUG("now urlcount:%s,kill pool start" % self.urlcount )
            self.pool.kill()
            DEBUG("kill pool end")

    def init_request(self):
        urls = self.task.get_exist_url()
        self.urlcount += len(urls)
        for url in urls:
            request = Request(url.url, url.method, url.params, url.referer)
            if self.visited[request] < self.duplicates:
                if not discard(request.url) and not url.end_time:
                    request.id = url.id
                    self.pendings.put(request)
                    DEBUG("-----request:%s not crawler,add queue" % request)
                self.visited[request] += 1
            else:
                #DEBUG("duplicates url:%s" %request)
                pass
        return self.urlcount     

                       
    def add_request(self, request):
        """
        0. judge discard or not,e.g. .css .png
        1. judge max depth
        2. judge whether duplicate
        3. judge max url count
        """
        if self.visited[request] < self.duplicates:
            self.judge_url_count()
            if not discard(request.url):
                request.id = pipeline(request)
                self.pendings.put(request)
                #DEBUG("--*--:%s" % request)
            else: #.png等url不放入队列
                pipeline(request)
            self.visited[request] += 1
        else:
            #DEBUG("duplicates url:%s" %request)
            pass        
 
    def is_origin(self,url):
        return url.startswith(self.domain)

    def parse_robots(self):
        """
        parse robots protocol,both allow and disallow entry
        for example: http://www.gaoloumi.com/robots.txt
        """
        self.task.update_robots_flag('start')
        robotsUrl = f"{self.domain}"+ "robots.txt"
        try:
            response = request.request(robotsUrl)
            if not response:
                return
            lines = response.text.splitlines() 
            for line in lines:
                match = ROBOTS_ALLOW_PATH.search(line)
                path = match.group('path') if match else '/'
                if path != '/':
                    url = urljoin(f"{self.domain}",path)
                    self.add_request(Request.from_url(url,robotsUrl))
        finally:
            self.task.update_robots_flag('finish')

    def parse_sitemap(self):
        """
        parse sitemap.xml
        for example: http://www.aouu.com/sitemap.xml
        """
        self.task.update_sitemap_parsed('start')
        sitemapUrl = f"{self.domain}" + "sitemap.xml"
        try:
            response = request.request(sitemapUrl)
            if not response:
                return
            lines = response.iter_lines() #sitemap.xml may very big
            for line in lines:
                match = SITEMAP_URL.search(line)
                if match:
                    url = match.group('url')
                    if self.is_origin(url) and url not in self.urlSet:
                        self.urlSet.add(url)
                        self.add_request(Request.from_url(url,sitemapUrl))
        finally:
            self.task.update_sitemap_parsed('finish')

    def do_schedule(self):
        DEBUG("Schedule start")
        self.task.update_spider_flag('start')
        while not self.stop and ( len(self.pool) > 0 or not self.pendings.empty()):
            try:
                request = self.pendings.get(block=False)
            except queue.Empty:
                gevent.sleep(0)
            else:
                self.pool.spawn(Spider.start,request,self)
                
        self.task.update_spider_flag('finish')
        code = (self.stop,self.urlcount,len(self.pool),self.pendings.qsize())
        DEBUG("Schedule end,stop:%s,now urlcount:%s,:pool size:%s,pendings size:%s" % code)
        #self.pool.join()



class Task(object):
    '''Task mysql Interaction
    '''
    def __init__(self, task_id):
        self.task_id = task_id

    def update_spider_flag(self, action):
        flag = {'start':1, 'finish':3}.get(action, 1)
        sql = "UPDATE task SET `spider_flag`=%s where id=%s"
        try:
            db.execute(sql, flag, self.task_id)
        except Exception:
            ERROR('update_spider_flag exception,task_id:%s' % self.task_id)

    def update_robots_flag(self, action):
        flag = {'start':0, 'finish':1}.get(action, 1)
        sql = "UPDATE task SET `robots_parsed`=%s where id=%s"
        try:
            db.execute(sql, flag, self.task_id)
        except Exception:
            ERROR('update_robots_flag exception,task_id:%s' % self.task_id)

    def update_sitemap_parsed(self, action):
        flag = {'start':0, 'finish':1}.get(action, 1)
        sql = "UPDATE task SET `sitemap_parsed`=%s where id=%s"
        try:
            db.execute(sql, flag, self.task_id)
        except Exception:
            ERROR('update_sitemap_parsed exception,task_id:%s' % self.task_id)

    def update_url_end_time(self, request):
        if request.id is not None:
            sql = "UPDATE url SET `end_time`=%s WHERE id=%s"
            try:
                db.execute(sql, datetime.now(), request.id)
            except Exception:
                ERROR('update_url_end_time exception,task_id:%s' % self.task_id)

    def get_exist_url(self):
        sql = "SELECT * FROM url WHERE task_id=%s"
        urls = None
        try:
            urls = [ url for url in db.iter(sql, self.task_id)]
        except Exception:
            ERROR('get_url exception,task_id:%s' % self.task_id)
        return urls or []


class CrawlEngine(object):
    @classmethod
    def start(cls):
        url = config.url
        basepath = config.base
        concurrency = 10
        depth = config.depth
        urlcount = config.count
        duplicates = 1
        assert url
        urls = list(url) if isinstance(url,(list,tuple)) else [url]
        schedule = Schedule(urls,concurrency,depth,urlcount,duplicates,basepath)
        DEBUG('CrawlEngine start')
        schedule.do_schedule()
        DEBUG('CrawlEngine end')
        
