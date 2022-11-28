import os
import sys
from typing import Any
from urllib.parse import urlparse
import gevent
from gevent.monkey import patch_all

from optparse import OptParseError
from optparse import OptionParser

from libs.core.data import cmdOptions ,config ,paths , SITETYPES
from libs.core.settings import CONNECTION_TIMEOUT, NETWORK_TIMEOUT, TASK_TABLE
#from libs.core.logs import ERROR, DEBUG, INFO
from libs.core.tools import mkdir, set_unreachable_flag
from libs.core.crawler import CrawlEngine
from libs.core.request import request
from libs.core.errors import DestinationUnReachable
from libs.utils import db

def get_target(task_id):
    sql = 'SELECT * FROM %s WHERE `ID`=%s' %(TASK_TABLE, task_id)
    task = db.get(sql)
    if not config.url:
        config.url = task.start_url
        config.base = task.base
        config.count = task.url_count
    config.finished_progress = task.progress.split('|') if config.goon else []
    config.robots_parsed = task.robots_parsed if config.goon else False
    config.sitemap_parsed = task.sitemap_parsed if config.goon else False
    config.spider_finish = True if config.goon and task.spider_flag == 3 else False


def _confsetting():
    config.update(cmdOptions)
   
    if not config.connect_timeout:
        config.connect_timeout = CONNECTION_TIMEOUT
    if not config.timeout:
        config.timeout = NETWORK_TIMEOUT

    get_target(config.taskid)

    parser = urlparse.urlsplit(config.url)
    config.host = parser.netloc
    config.scheme = parser.scheme
    config.domain = "%s://%s%s" % (parser.scheme, parser.netloc,config.base)
    config.requestCache = os.path.join(f"{paths.TEMP}",config.host)
    config.site_type = None
    print(config)

def _geventpatch():
    """
    do monkey.patch_all carefully
    """
    patch_all(socket=True, dns=True, time=True, select=True, thread=False, os=True, ssl=True, httplib=False,
              subprocess=False, sys=False, aggressive=True, Event=False)

_dnscache = {}
def _setDnsCache():
    """
    set dns cache for socket.getaddrinfo and gevent to avoid subsequent DNS requests 
    """
    def _getaddrinfo(*args, **kwargs):
        if args in _dnscache:
            #DEBUG(str(args)+' in cache')
            return _dnscache[args]

        else:
            #DEBUG(str(args)+' not in cache')
            _dnscache[args] = gevent.socket._getaddrinfo(*args, **kwargs)
            return _dnscache[args]

    if not hasattr(gevent.socket, '_getaddrinfo'):
        gevent.socket._getaddrinfo = gevent.socket.getaddrinfo
        gevent.socket.getaddrinfo = _getaddrinfo

def _mkcachedir():
    mkdir(config.request_cache)

#def changesysEncoding(encodeing='utf-8'):
#    try:
#        import sys
#        reload(sys)
#        sys.setdefaultencoding(encodeing)
#    except ImportError:
#        import importlib, sys
#        importlib.reload(sys)
#        sys.setdefaultencoding(encodeing)


def destReachable(dest: Any = None):
    if not dest:
        dest = config.url

    response = request(dest,timeout=config.connect_timeout)
    if response is None:
        set_unreachable_flag(config.taskid)
        raise DestinationUnReachable(dest)
    else:
        config.site_type = sitetype_check(response)

def check_type(msg):
    for k in SITETYPES.keys():
        if msg.find(k) != -1:
            return k

def sitetype_check(response):
    site_type = None
    if 'x-powered-by' in response.headers:
        site_type = check_type(response.headers['x-powered-by'].upper())
    if site_type is None:
        if 'server' in response.headers:
            site_type = check_type(response.headers['server'].upper())
    return site_type
    
def init():
    _confsetting()
    _mkcachedir()
    _geventpatch()
    _setDnsCache()
    #changesysEncoding()
    destReachable()

def run():
    CrawlEngine.start()


def parseCmdline():
    """
    parse command line parameters and arguments and store in cmdLineOptions
    """
    usage = "%s %s [options]" %("python",sys.argv[0])
    parser = OptionParser(usage=usage)
    parser.add_option("-t","--task",dest="taskid",help="task id")
    parser.add_option("-u","--url",dest="url",help="target url")
    parser.add_option("-b","--base",dest="base",default="/",help="the base directory of the domain")
    parser.add_option("-d","--depth",dest="depth",type="int",default=0,help="crawl depth")
    parser.add_option("-c","--count",dest="count",type="int",default=0,help="crawl url max count")
    parser.add_option("--cookie",dest="cookie",help="http cookie header")
    parser.add_option("--connect_timeout",dest="connect_timeout",help="set connect timeout")
    parser.add_option("--timeout",dest="timeout",help="network timeout")
    parser.add_option("--continue",action="store_true",dest="goon",help="task continue run")
    try:
        args,_ = parser.parse_args(sys.argv[1:])
        cmdOptions.update(args.__dict__)
        print(cmdOptions)
    except OptParseError:
        print(parser.error("parse command line error !"))
        


