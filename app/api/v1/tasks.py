from flask import Blueprint, request, jsonify
from app.models.tasks import Task
from app.models.urls import URL
from app.scanner.engine import ScanEngine
from app.libs.error_codes import Success
from app.validators.forms import TaskCreateForm
from app.libs.enums import TaskStatus

tasks = Blueprint('tasks', __name__)

@tasks.route('/tasks', methods=['POST'])
def create_task():
    """创建扫描任务"""
    form = TaskCreateForm().validate_for_api()
    
    task = Task()
    task.name = form.name.data
    task.target_url = form.target_url.data
    task.scan_policy = form.scan_policy.data
    task.save()
    
    # 创建URL记录
    url = URL()
    url.url = form.target_url.data
    url.task_id = task.id
    url.save()
    
    return Success(msg='创建任务成功')

@tasks.route('/tasks', methods=['GET'])
def get_tasks():
    """获取任务列表"""
    page = request.args.get('page', 1, type=int)
    size = request.args.get('size', 10, type=int)
    status = request.args.get('status', None, type=str)
    
    query = Task.query
    if status:
        query = query.filter_by(status=status)
    
    pagination = query.order_by(Task.create_time.desc()).paginate(
        page=page, per_page=size, error_out=False)
    
    tasks = pagination.items
    total = pagination.total
    
    return jsonify({
        'code': 0,
        'msg': '获取任务列表成功',
        'data': {
            'total': total,
            'items': [task.to_dict() for task in tasks]
        }
    })

@tasks.route('/tasks/<int:task_id>/start', methods=['POST'])
def start_task(task_id):
    """启动扫描任务"""
    task = Task.query.get_or_404(task_id)
    
    if task.status != TaskStatus.PENDING:
        return jsonify({
            'code': 400,
            'msg': '任务状态不正确，只有待执行的任务可以启动'
        })
    
    # 使用Celery异步执行扫描任务
    from app.tasks.tasks import execute_scan_task
    execute_scan_task.delay(task_id)
    
    return Success(msg='启动任务成功')

@tasks.route('/tasks/<int:task_id>/status', methods=['GET'])
def get_task_status(task_id):
    """获取任务状态"""
    task = Task.query.get_or_404(task_id)
    
    # 获取任务相关的URL总数
    url_count = URL.query.filter_by(task_id=task_id).count()
    
    # 获取发现的漏洞数量
    vulnerability_count = ResultModel.query.filter_by(task_id=task_id).count()
    
    return jsonify({
        'code': 0,
        'msg': '获取任务状态成功',
        'data': {
            'id': task.id,
            'name': task.name,
            'status': task.status,
            'start_time': task.start_time,
            'end_time': task.end_time,
            'url_count': url_count,
            'vulnerability_count': vulnerability_count
        }
    })