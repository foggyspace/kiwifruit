import re
from collections import namedtuple

GET, POST = "GET", "POST"
DEFAULT_METHOD = "GET"
PARAMS_PATTERN = re.compile("(?P<key>[^&=]+)(?:=(?P<value>[^&=]*))?")
TITLE_PATTERN = re.compile("<title>(?P<title>[^<]+)</title>", re.I)

SITETYPES = {"PHP": ".php", "JSP": ".jsp", "ASP": ".asp", "ASP.NET": ".asp"}


class ObjectDict(dict):
    def __getattr__(self, item):
        try:
            return self[item]
        except KeyError:
            raise AttributeError(item)

    def __setattr__(self, key, value):
        self[key] = value

paths = ObjectDict()

conf = ObjectDict()

commandline_options = ObjectDict()


class Url(object):
    def __init__(self, url, method, params, referer):
        self.url = url
        self.method = method
        self.params = params
        self.referer = referer

    @classmethod
    def from_url(cls, url, referer):
        url, params = url.split('?', 1) if url.find('?') else (url, '')
        return cls(url, DEFAULT_METHOD, params, referer)

    @property
    def name(self):
        return self.__class__.__name__

    def __str__(self):
        return f"<{self.name}, {self.url}, {self.method}, {self.params}, {self.referer}>"

    __repr__ = __str__


Result = namedtuple("Result", "response details")