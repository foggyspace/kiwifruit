import hmac
import json
import time

from urllib.parse import urlsplit

import gevent
from gevent import monkey
monkey.patch_socket()

from icepie.app_site.models import Task

ADDRESS = ("localhost", 6667)


def get_domain(task_id):
    task = Task.objects.get(task_id)
    _ = urlsplit(task.start_url)
    domain = "%s://%s%s" % (_.scheme, _.netloc, task.base)
    return domain


def json_success(msg=""):
    data = {"success": True, "msg": msg}
    return json.dumps(data)


def json_error(msg=""):
    data = {"success": False, "msg": msg}
    return json.dumps(data)


def enum(*sequential, **named):
    start = named.pop("start", 0)
    end = len(sequential) + start
    enums = dict(zip(sequential, range(start, end)), **named)
    return type("Enum", (), enums)


SECRE_KEY = {
    "SCAN_MODULE": "_K_ICEPIE_***_SCANNER"
}


def send_request(module_name, request_headers):
    try:
        key = SECRE_KEY.get(module_name, "UNKNOWN_KEY")
        socket = gevent.socket.socket()
        socket.connect(ADDRESS)
        request_headers["module"] = module_name
        request_headers["signature"] = hmac.new(key, module_name).hexdigest()
        h = ["%s:%s" % (k, v) for k, v in request_headers.items()]
        h.append("\n")
        request = "\n".join(h)
        socket.send(bytes(request))
        content = socket.recv(8192)
        time.sleep(2)
        socket.close()
        return json.loads(content)
    except Exception:
        return {"success": False, "msg": "send request error"}
