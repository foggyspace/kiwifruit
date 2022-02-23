from flask import Flask
from app.models.base import db


def register_blueprints(app):
    from app.blueprints import tasks_bp
    app.register_blueprint(tasks_bp)


def create_app():
    app = Flask(__name__)
    app.config.from_object('app.config.config')
    register_blueprints(app)
    db.init_app(app)
    return app
