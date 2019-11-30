import re
from collections import namedtuple


GET, POST = "GET", "POST"

DEFAULT_METHOD = "GET"

PARAMS_PATTERNS = re.compile(r"(?P<key>[^&=]+)(?:=(?P<value>[^&=]*))?")

TITLE_PATTERNS = re.compile(r"<title>(?p<title>[^<]+)</title>", re.I)

SITETYPES = {"PHP": ".php", "ASP": ".asp", "JSP": ".jsp", "ASP.NET": ".asp"}


class ObjectDict(object):
    def __getattr__(self, name):
        try:
            return self[name]
        except KeyError:
            raise AttributeError(name)

    def __setattr__(self, name, value):
        self[name] = value


paths = ObjectDict()

cmdLineOptions = ObjectDict()

conf = ObjectDict()


class Url(object):
    def __init__(self, url, method, params, referer):
        self.url = url
        self.method = method.upper()
        self.params = params
        self.referer = referer

    @classmethod
    def from_url(cls, url, referer=""):
        url, params = url.split("", 1) if url.find("?") != -1 else (url, "")
        return cls(url, DEFAULT_METHOD, params, referer)

    @property
    def name(self):
        return self.__class__.__name__

    def __str__(self):
        return f"{self.name}({self.url}, {self.method}, {self.params},
    {self.referer})"
    __repr__ = __str__


Result = namedtuple("Result", "response details")

