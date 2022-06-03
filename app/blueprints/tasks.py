from pytz import utc
from flask import Blueprint, render_template, request, jsonify
from app.extensions import apscheduler
from app.utils.common import parse_crontab


def _run():
    ...


tasks_bp = Blueprint('tasks_bp', __name__)


def init_job(scheduler, **data):
    job_id = data.get('job_id')
    trigger_type = data.get('trigger_type')

    if trigger_type == 'date':
        run_date = data.get('run_date')
        scheduler.add_job(_run, id=job_id, trigger='date', run_date=run_date, replace_existing=True)
        return job_id
    elif trigger_type == 'interval':
        interval = data.get('interval')
        scheduler.add_job(_run, id=job_id, trigger='interval', minutes=interval, replace_existing=True)
        return job_id
    elif trigger_type == 'cron':
        cron = data.get('cron')
        crontab = parse_crontab(cron)
        if not crontab:
            return None
        minute, hour, day, month, day_of_week = crontab
        scheduler.add_job(_run, id=job_id, trigger='cron', minute=minute, hour=hour, day=day, month=month, day_of_week=day_of_week,
                replace_existing=True)
        return job_id
    else:
        return None



@tasks_bp.route('/index')
@tasks_bp.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@tasks_bp.route('/list', methods=['GET'])
def list():
    return render_template('list.html')


@tasks_bp.route('/add', methods=['POST'])
def add_job():
    data = request.get_json(force=True)
    job_id = init_job(apscheduler, *data)
    return jsonify({
        'msg': 'add success',
        'code': 200,
        'job_id': job_id
        })



@tasks_bp.route('/get', methods=['GET'])
def get_job():
    pass


@tasks_bp.route('/remove', methods=['POST'])
def remove_job():
    job_id = request.args.get('job_id')
    apscheduler.remove_job(job_id)
    return jsonify({
        'msg': 'remove success',
        'code': 200
        })


@tasks_bp.route('/resume', methods=['POST'])
def resume_job():
    job_id = request.args.get('job_id')
    apscheduler.resume_job(job_id)
    return jsonify({
        'msg': 'resume success',
        'code': 200
        })


@tasks_bp.route('/pause', methods=['POST'])
def pause_job():
    job_id = request.args.get('job_id')
    apscheduler.pause_job(job_id)
    return jsonify({
        'msg': 'pause success',
        'code': 200
        })
