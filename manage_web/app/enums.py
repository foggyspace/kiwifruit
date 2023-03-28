from enum import Enum


class TaskStatusEnum(Enum):
    """ 任务运行状态
        WAIT = "WAIT"
        RUNNING = "RUNNING"
        STOP = "STOP"
        FINISH = "FINISH"
    """
    WAIT = 0
    RUNNING = 1
    STOP = 2
    FINISH = 3


class SpiderStausEnum(Enum):
    """爬虫运行状态
        WAIT = "WAIT"
        RUNNING = "RUNNING"
        STOP = "STOP"
        FINISH = "FINISH"
    """
    WAIT = 0
    RUNNING = 1
    STOP = 2
    FINISH = 3


class RiskLevelEnum(Enum):
    """漏洞风险等级
        LOW = "LOW"
        MIDDLE = "MIDDLE"
        HIGH = "HIGH"
    """
    LOW = 0
    MIDDLE = 1
    HIGH = 2

