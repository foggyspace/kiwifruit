from typing import Any
from flask import Blueprint


class ApiPrint(object):
    def __init__(self, name: str) -> None:
        self.name = name
        self.mount = []

    def route(self, rule: str, **options):
        def decorator(f):
            self.mount.append((f, rule, options))
            return f
        return decorator

    def register(self, bp: Blueprint, url_prefix: Any = None):
        if url_prefix is None:
            url_prefix = '/' + self.name
        for f, rule, options in self.mount:
            endpoint = self.name + '+' + options.pop('endpoint', f.__name__)
            bp.add_url_rule(url_prefix + rule, endpoint, f, **options)

