from flask import Flask
from app.extensions import db, login_manager, migrate
from app.configs import config


def create_app(config_name=None):
    if config_name is None:
        config_name = 'development'
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    register_blueprints(app)
    register_extensions(app)
    return app


def register_blueprints(app):
    from app.blueprints.admin import admin
    from app.blueprints.auth import auth_bp
    app.register_blueprint(admin)
    app.register_blueprint(auth_bp)


def register_extensions(app):
    db.init_app(app)
    with app.app_context():
        db.create_all()
    login_manager.init_app(app)
    migrate.init_app(app, db)

