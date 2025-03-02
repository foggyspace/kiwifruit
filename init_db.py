from app import create_app
from app.models.base import db
from app.models.users import User
from app.models.tasks import Task
from app.models.urls import URLModel
from app.models.vulnerabilities import VulnerabilityModel
from app.models.results import ResultModel

app = create_app()

with app.app_context():
    # 删除所有已存在的表
    db.drop_all()
    
    # 创建所有表
    db.create_all()
    
    # 创建默认管理员用户
    admin = User()
    admin.email = 'admin@example.com'
    admin.nickname = 'admin'
    admin.password = 'admin123'
    admin.role = 1  # 设置为管理员角色
    
    with db.auto_commit():
        db.session.add(admin)
    
    print('数据库表创建成功！')
    print('默认管理员账号创建成功！用户名：admin@example.com，密码：admin123')