#from app import celery_init_app, create_app
from app import create_app

flask_app = create_app()
celery_app = flask_app.extensions['celery']
#celery_app = celery_init_app(flask_app)

