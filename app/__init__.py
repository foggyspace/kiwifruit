from flask import Flask
from celery import Celery, Task


def celery_init_app(app: Flask) -> Celery:
    class FlaskTask(Task):
        def __call__(self, *args: object, **kwargs: object) -> object:
            with app.app_context():
                return self.run(*args, **kwargs)
    celery_app = Celery(app.name, task_cls=FlaskTask, broker='redis://localhost:6379/0', include=['app.tasks.tasks'])
    #celery_app.config_from_object(app.config['CELERY'])
    celery_app.set_default()
    app.extensions['celery'] = celery_app
    return celery_app


def register_blueprints(app: Flask) -> None:
    from app.api.v1 import create_blueprint_v1

    app.register_blueprint(create_blueprint_v1(), url_prefix='/v1')


def register_plugins(app: Flask) -> None:
    pass


def create_app() -> Flask:
    app = Flask(__name__)
    #app.config.from_mapping(
    #    CELERY=dict(
    #        broker_url='redis://localhost:6379/0',
    #        result_backend='redis://localhost:6379/1',
    #        task_ignore_result=True,
    #    ),
    #)
    celery_init_app(app)
    register_blueprints(app)
    return app


