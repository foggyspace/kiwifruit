from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate


db = SQLAlchemy()

login_manager = LoginManager()

migrate = Migrate()


@login_manager.user_loader
def load_user(user_id):
    from app.models.admin import Admin
    user = Admin.query.get(int(user_id))
    return user


login_manager.login_view = 'auth.login'
login_manager.login_message_category = 'warning'

