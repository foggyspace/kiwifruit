from sqlalchemy import Column, Integer, String, SmallInteger
from werkzeug.security import generate_password_hash, check_password_hash

from app.models.base import BaseModel


class User(BaseModel):
    id = Column(Integer, primary_key=True)
    email = Column(String(24), unique=True, nullable=False)
    nickname = Column(String(24), unique=True)
    auth = Column(SmallInteger, default=1)
    _password = Column('password', String(128))

    @property
    def password(self):
        return self._password

    @property.setter
    def password(self, raw: str):
        self._password = generate_password_hash(raw)

    def check_password(self, raw: str) -> bool:
        if not self._password:
            return False
        return check_password_hash(self._password, raw)

    @staticmethod
    def verify(email: str, password: str) -> dict:
        user = User.query.filter_by(email=email).first_or_404()
        if not user.check_password(password):
            raise Exception()
        permission = 'Admin' if user.auth == 2 else 'Guest'
        return {'uuid': user.id, 'permission': permission}

