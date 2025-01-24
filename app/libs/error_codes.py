from enum import Enum
from typing import Dict, Any


class ErrorCode(Enum):
    """错误码枚举类
    
    规则：
    - 0 表示成功
    - 1-100 为通用错误码
    - 101-200 为认证相关错误码
    - 201-300 为参数相关错误码
    - 301-400 为业务相关错误码
    """
    # 通用错误码 (1-100)
    SUCCESS = (0, 200, "success", "操作成功")
    FAILED = (1, 400, "failed", "操作失败")
    SERVER_ERROR = (2, 500, "server error", "服务器内部错误")
    NOT_FOUND = (4, 404, "not found", "资源未找到")
    
    # 认证相关错误码 (101-200)
    AUTH_FAILED = (101, 401, "authentication failed", "认证失败")
    FORBIDDEN = (102, 403, "forbidden", "禁止访问")
    INVALID_TOKEN = (103, 401, "invalid token", "无效的令牌")
    EXPIRED_TOKEN = (104, 401, "expired token", "令牌已过期")
    
    # 参数相关错误码 (201-300)
    PARAMETER_ERROR = (201, 400, "parameter error", "参数错误")
    VALIDATION_ERROR = (202, 400, "validation error", "数据验证错误")
    
    def __init__(self, error_code: int, http_code: int, en_msg: str, zh_msg: str) -> None:
        self._error_code = error_code
        self._http_code = http_code
        self._en_msg = en_msg
        self._zh_msg = zh_msg
    
    @property
    def error_code(self) -> int:
        return self._error_code
    
    @property
    def http_code(self) -> int:
        return self._http_code
    
    @property
    def en_msg(self) -> str:
        return self._en_msg
    
    @property
    def zh_msg(self) -> str:
        return self._zh_msg
    
    def to_dict(self, lang: str = 'zh') -> Dict[str, Any]:
        return {
            'error_code': self.error_code,
            'msg': self.zh_msg if lang == 'zh' else self.en_msg
        }