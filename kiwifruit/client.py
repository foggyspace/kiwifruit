import hmac
import gevent
from gevent import monkey
monkey.patch_socket()

ADDRESSES = ("localhost", 6667)


def send_command():
    socket = gevent.socket.socket()
    socket.connect(ADDRESSES)
    s = "module:SCAN_MODULE\naction:start\n\n"
    print(s)
    socket.send(s)
    print("[+] send over")
    print(socket.recv(1024))
    socket.close()


def send_request(module_name, request_headers):
    SECRE_KEY = "_KIWIFUIT_**_SCANNER_"
    socket = gevent.socket.socket()
    socket.connect(ADDRESSES)
    request_headers["module"] = module_name
    request_headers["signature"] = hmac.new(SECRE_KEY, module_name).hexdigest()
    h = ["%s:%s" % (k, v) for k, v in request_headers.items()]
    h.append("\n")
    request = "\n".join(h)
    socket.send(bytes(request))
    print(socket.recv(8192))
    socket.close()


