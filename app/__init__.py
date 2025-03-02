from flask import Flask
from celery import Celery, Task


def celery_init_app(app: Flask) -> Celery:
    class FlaskTask(Task):
        def __call__(self, *args: object, **kwargs: object) -> object:
            with app.app_context():
                return self.run(*args, **kwargs)
    celery_app = Celery(app.name, task_cls=FlaskTask)
    celery_app.config_from_object('app.config.celeryconfig')
    celery_app.set_default()
    app.extensions['celery'] = celery_app
    return celery_app


def register_blueprints(app: Flask) -> None:
    from app.api.v1 import create_blueprint_v1
    app.register_blueprint(create_blueprint_v1(), url_prefix='/api/v1')


def register_plugins(app: Flask) -> None:
    from flask_migrate import Migrate
    from flask_cors import CORS
    from flask_jwt_extended import JWTManager
    from app.models.base import db
    
    # 初始化数据库
    db.init_app(app)
    
    # 初始化数据库迁移
    Migrate(app, db)
    
    # 初始化CORS
    CORS(app)
    
    # 初始化JWT
    JWTManager(app)


def create_app() -> Flask:
    app = Flask(__name__)
    
    # 加载配置
    app.config.from_object('app.config.settings')
    
    # 根据环境变量加载不同的配置
    env = app.config.get('ENV', 'development')
    if env == 'production':
        app.config.from_object('app.config.Production')
    else:
        app.config.from_object('app.config.Developments')
    
    celery_init_app(app)
    register_plugins(app)
    register_blueprints(app)
    return app


