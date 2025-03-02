from sqlalchemy import Column, Integer, String, SmallInteger
from werkzeug.security import generate_password_hash, check_password_hash
from app.models.base import BaseModel

# 定义权限常量
class Permissions:
    # 普通用户权限
    GENERAL = 0x01
    # 日志审计权限
    AUDIT = 0x02
    # 管理员权限
    ADMIN = 0x04

# 定义角色和对应权限
class Roles:
    USER = ('User', Permissions.GENERAL)
    AUDITOR = ('Auditor', Permissions.GENERAL | Permissions.AUDIT)
    ADMIN = ('Admin', Permissions.GENERAL | Permissions.AUDIT | Permissions.ADMIN)

class User(BaseModel):
    id = Column(Integer, primary_key=True)
    email = Column(String(24), unique=True, nullable=False)
    nickname = Column(String(24), unique=True)
    role = Column(String(24), default=Roles.USER[0])
    permissions = Column(Integer, default=Roles.USER[1])
    _password = Column('password', String(128))

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, raw: str):
        self._password = generate_password_hash(raw)

    def check_password(self, raw: str) -> bool:
        if not self._password:
            return False
        return check_password_hash(self._password, raw)

    def can(self, permission) -> bool:
        return self.permissions & permission == permission

    @property
    def is_admin(self) -> bool:
        return self.can(Permissions.ADMIN)

    @property
    def is_auditor(self) -> bool:
        return self.can(Permissions.AUDIT)

    @staticmethod
    def verify(username: str, password: str) -> dict:
        # 支持用户名或邮箱登录
        user = User.query.filter(
            (User.email == username) | (User.nickname == username)
        ).first()
        if not user:
            return None
        if not user.check_password(password):
            return None
        return {
            'uuid': user.id,
            'permission': user.role,
            'is_admin': user.is_admin,
            'is_auditor': user.is_auditor
        }

    def set_role(self, role_name: str) -> None:
        """设置用户角色"""
        role = getattr(Roles, role_name.upper(), None)
        if role:
            self.role = role[0]
            self.permissions = role[1]

