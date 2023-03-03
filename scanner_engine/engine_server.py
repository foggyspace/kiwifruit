from typing import Any

from email import message_from_file

from gevent.server import StreamServer
from gevent.subprocess import Popen, call

from lib.core.logs import ERROR, INFO, WARN


PLUGINS_MODULES = {} # 将所有的扫描器插件加载到这个字典里

SERVER_ADDRESS = ("127.0.0.1", 9527)


def register_plugins(name: str, handler: Any):
    """注册漏洞扫描插件"""
    if name in PLUGINS_MODULES:
        WARN(f"duplicate module name : {name}")
    else:
        PLUGINS_MODULES[name] = handler


class EngineServer:
    read_buffer_size = -1
    write_buffer_size = 0

    def start(self):
        """开启服务监听"""
        INFO("[engine] wait connection...")
        self.server = StreamServer(SERVER_ADDRESS, self.tcp_handler)
        self.server.start()

    def stop(self):
        """停止服务"""
        self.server.stop()

    def tcp_handler(self, sockfd, address):
        """处理tcp请求"""
        try:
            r = sockfd.makefile("rb", self.read_buffer_size)
            w = sockfd.makefile("wb", self.write_buffer_size)
            headers = message_from_file(r)

            INFO(f"connection from : {address} - headers : {headers}")
        except Exception:
            ERROR("tcp handler exception, please check.")



class Plugin:
    SECURE_KEY = "_KIWIFRUIT_SCANNER_"
    PLUGIN_NAME = "BASE_SCAN"

    def __init__(self, r, headers) -> None:
        self.r = r
        self.headers = headers


class ScannerPlugin(Plugin):
    """扫描器插件类用于启动扫描器插件"""
    PLUGIN_NAME = "SCAN_PLUGIN"

    def start_scan(self, options: str):
        """开始扫描器"""
        pass

    def resume_scan(self):
        """接着扫描"""
        pass

    def cancel_scan(self):
        """关闭扫描器"""
        pass


def main():
    register_plugins(ScannerPlugin.PLUGIN_NAME, ScannerPlugin)
    engine_server = EngineServer()
    engine_server.start()


if __name__ == "__main__":
    main()

