from flask import Flask

from flask_admin import Admin


def create_app():
    app = Flask(__name__)

    app.config["FLASK_ADMIN_SWATCH"] = "cerulean"

    register_bluerpint_views(app)
    register_flask_plugin(app)
    register_flask_admin(app)

    return app


def register_bluerpint_views(app: Flask):
    """注册Flask蓝图对象"""


def register_flask_admin(app: Flask):
    """注册flask Admin"""
    admin = Admin(name="webscanner", template_mode="bootstrap3")
    admin.init_app(app=app)


def register_flask_plugin(app: Flask):
    """注册flask插件"""

