from abc import ABC, abstractmethod
from enum import Enum
from typing import Any, Dict, List, Optional
from dataclasses import dataclass
import requests


class RiskLevel(Enum):
    """漏洞风险等级"""
    LOW = "低危"
    MEDIUM = "中危"
    HIGH = "高危"
    CRITICAL = "严重"


@dataclass
class VulnerabilityInfo:
    """漏洞信息数据类"""
    name: str
    description: str
    risk_level: RiskLevel
    solution: str
    references: List[str]
    details: Dict[str, Any]


class PluginABC(ABC):
    """插件抽象基类"""
    def __init__(self):
        self.name = self.__class__.__name__
        self.description = "插件描述"
        self.enabled = True
        self.priority = 0
        self.session = requests.Session()

    @abstractmethod
    def run(self, target: str) -> Optional[VulnerabilityInfo]:
        """执行漏洞检测
        Args:
            target: 目标URL或其他目标标识
        Returns:
            如果发现漏洞，返回漏洞信息；否则返回None
        """
        pass

    def send_request(self, url: str, method: str = "GET", **kwargs) -> requests.Response:
        """发送HTTP请求的工具方法"""
        return self.session.request(method, url, **kwargs)

    def parse_response(self, response: requests.Response) -> Dict[str, Any]:
        """解析HTTP响应的工具方法"""
        return {
            "status_code": response.status_code,
            "headers": dict(response.headers),
            "content": response.text,
            "content_type": response.headers.get("content-type", "")
        }

    def __str__(self) -> str:
        return f"{self.name} - {self.description}"