from pytz import utc
from flask import Blueprint
from apscheduler.schedulers.background import BackgroundScheduler
from app.config.settings import executors


scheduler = None

tasks_bp = Blueprint('tasks_bp', __name__)


def start_scheduler():
    global scheduler
    scheduler = BackgroundScheduler(executors=executors, timezone=utc)
    scheduler.start()


start_scheduler()


def run_scanner():
    pass


@tasks_bp.route('/index')
@tasks_bp.route('/', methods=['GET'])
def index():
    return 'index page'


@tasks_bp.route('/addJob', methods=['GET', 'POST'])
def add_job():
    pass


@tasks_bp.route('getJob', methods=['GET'])
def get_job():
    pass
