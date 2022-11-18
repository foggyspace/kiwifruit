from flask import Flask
from app.extensions import db, apscheduler


def register_blueprints(app):
    from app.blueprints import tasks_bp
    app.register_blueprint(tasks_bp)


def register_plugins(app):
    db.init_app(app)
    apscheduler.init_app(app)


def create_app():
    app = Flask(__name__)
    app.config.from_object('app.config.config')
    register_blueprints(app)
    register_plugins(app)
    return app
