from app import create_app
from celery.signals import worker_ready, worker_shutdown, task_failure
import logging

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 创建Flask应用和Celery实例
flask_app = create_app()
celery_app = flask_app.extensions['celery']

# 配置Celery Worker
celery_app.conf.update(
    worker_concurrency=4,  # 设置worker进程数
    task_routes={
        'app.tasks.*': {'queue': 'default'}  # 设置任务路由
    },
    task_reject_on_worker_lost=True,  # 当worker意外终止时重试任务
    task_acks_late=True  # 任务执行完成后再确认
)

# Celery信号处理
@worker_ready.connect
def worker_ready_handler(sender=None, **kwargs):
    logger.info('Celery worker is ready and listening for tasks')

@worker_shutdown.connect
def worker_shutdown_handler(sender=None, **kwargs):
    logger.info('Celery worker is shutting down')

@task_failure.connect
def task_failure_handler(sender=None, task_id=None, exception=None, **kwargs):
    logger.error(f'Task {task_id} failed: {str(exception)}')

