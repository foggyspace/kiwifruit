from app import create_app
from app.models.base import db


app = create_app()


with app.app_context():
    db.create_all()


if __name__ == '__main__':
    app.run()
