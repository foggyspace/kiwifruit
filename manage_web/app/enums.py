from enum import Enum


class TaskStatusEnum(Enum):
    """ 任务运行状态"""
    WAIT = "WAIT"
    RUNNING = "RUNNING"
    STOP = "STOP"
    FINISH = "FINISH"


class SpiderStausEnum(Enum):
    """爬虫运行状态"""
    WAIT = "WAIT"
    RUNNING = "RUNNING"
    STOP = "STOP"
    FINISH = "FINISH"


class RiskLevelEnum(Enum):
    """漏洞风险等级"""
    LOW = "LOW"
    MIDDLE = "MIDDLE"
    HIGH = "HIGH"

