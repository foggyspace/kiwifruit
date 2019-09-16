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