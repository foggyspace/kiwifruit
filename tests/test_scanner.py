import unittest
from unittest.mock import Mock, patch
import gevent
from gevent import queue
from app.scanner.engine import ScanEgine
from app.plugins.base import PluginABC, VulnerabilityInfo, RiskLevel


class MockPlugin(PluginABC):
    def __init__(self):
        super().__init__()
        self.name = "MockPlugin"
        self.enabled = True

    def run(self, target):
        if "vulnerable" in target:
            return VulnerabilityInfo(
                name="测试漏洞",
                description="这是一个测试漏洞",
                risk_level=RiskLevel.HIGH,
                solution="修复测试漏洞",
                references=["http://test.com"],
                details={"test": "details"}
            )
        return None


class TestScanEngine(unittest.TestCase):
    def setUp(self):
        self.task_id = 1
        self.start_url = "http://test.com"
        self.engine = ScanEgine(self.task_id, self.start_url)
        # 模拟插件管理器
        self.engine.plugin_manager.get_plugins = Mock(return_value=[MockPlugin()])

    def test_scan_url_with_vulnerability(self):
        """测试扫描包含漏洞的URL"""
        test_url = "http://test.com/vulnerable"
        with patch('app.models.results.ResultModel.save') as mock_save:
            self.engine._scan_url(test_url)
            mock_save.assert_called_once()
            self.assertIn(test_url, self.engine.scanned_urls)

    def test_scan_url_without_vulnerability(self):
        """测试扫描不包含漏洞的URL"""
        test_url = "http://test.com/safe"
        with patch('app.models.results.ResultModel.save') as mock_save:
            self.engine._scan_url(test_url)
            mock_save.assert_not_called()
            self.assertIn(test_url, self.engine.scanned_urls)

    def test_scheduler_url(self):
        """测试URL调度器"""
        test_url = "http://test.com/test"
        self.engine.url_queue.put(test_url)
        
        # 启动调度器
        gevent.spawn(self.engine.schedulerURL)
        # 等待URL被处理
        gevent.sleep(2)
        
        self.assertIn(test_url, self.engine.scanned_urls)

    def test_duplicate_url_handling(self):
        """测试重复URL处理"""
        test_url = "http://test.com/duplicate"
        self.engine.scanned_urls.add(test_url)
        
        with patch('app.models.results.ResultModel.save') as mock_save:
            self.engine._scan_url(test_url)
            mock_save.assert_not_called()

    def test_error_handling(self):
        """测试异常处理"""
        def mock_plugin_with_error():
            raise Exception("测试异常")

        test_url = "http://test.com/error"
        mock_plugin = MockPlugin()
        mock_plugin.run = mock_plugin_with_error
        self.engine.plugin_manager.get_plugins = Mock(return_value=[mock_plugin])

        try:
            self.engine._scan_url(test_url)
            self.assertIn(test_url, self.engine.scanned_urls)
        except Exception:
            self.fail("异常处理失败")


if __name__ == '__main__':
    unittest.main()