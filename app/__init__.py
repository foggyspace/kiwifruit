from flask import Flask


def register_blueprints(app):
    from app.blueprints import tasks_bp
    app.register_blueprint(tasks_bp)


def create_app():
    app = Flask(__name__)
    register_blueprints(app)
    return app
