import gevent
import time
from gevent import pool, queue, spawn, joinall
from typing import Set, Dict, Any, Optional
from app.models.urls import URLModel
from app.models.vulnerabilities import VulnerabilityModel
from app.plugins.manager import PluginManager
from app.models.results import ResultModel


class ScanEgine(object):
    def __init__(self, task_id: int, start_url: str) -> None:
        self.pool: pool.Pool = pool.Pool(10)
        self.task_id = task_id
        self.host = ''
        self.plugin_manager = PluginManager()
        self.scanned_urls: Set[str] = set()
        self.url_queue = queue.Queue()
        self.crawler = CrawlerSpider(start_url, task_id)

    def start(self) -> None:
        joinall([
            spawn(self.crawler.crawl),
            spawn(self.schedulerURL)
        ])

        self.pool.join()

    def _save_vulnerability(self, url: str, plugin_name: str, vul_info: Dict[str, Any]) -> None:
        """保存漏洞信息到数据库"""
        if not vul_info:
            return

        result = ResultModel()
        result.task_id = self.task_id
        result.url = url
        result.vul_type = vul_info.get('type', '')
        result.description = vul_info.get('description', '')
        result.severity = vul_info.get('severity', 0)
        result.solution = vul_info.get('solution', '')
        result.reproduce_steps = vul_info.get('reproduce_steps', '')
        result.risk = vul_info.get('risk_level', 0)
        result.proof = str(vul_info.get('details', {}))
        result.request = vul_info.get('request', '')
        result.response = vul_info.get('response', '')
        result.discover_time = int(time.time())
        result.save()

    def _scan_url(self, url: str) -> None:
        """对单个URL执行漏洞扫描"""
        if url in self.scanned_urls:
            return

        for plugin in self.plugin_manager.get_plugins():
            try:
                vul_info = plugin.run(url)
                if vul_info:
                    self._save_vulnerability(url, plugin.name, vul_info)
            except Exception as e:
                print(f"Error running plugin {plugin.name} on {url}: {str(e)}")

        self.scanned_urls.add(url)

    def schedulerURL(self) -> None:
        """调度URL扫描任务"""
        while True:
            try:
                # 从爬虫队列中获取URL
                url = self.url_queue.get(timeout=1)  # 设置1秒超时
                if url and url not in self.scanned_urls:
                    self.pool.spawn(self._scan_url, url)
            except queue.Empty:
                # 队列为空时等待
                gevent.sleep(1)
            except Exception as e:
                print(f"Error in URL scheduler: {str(e)}")
                gevent.sleep(1)

    def schedulerDomain(self) -> None:
        """域名扫描调度器，待实现"""
        pass


def run(task_id: int, start_url: str) -> None:
    engine = ScanEgine(task_id, start_url)
    engine.start()

