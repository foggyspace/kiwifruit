from celery import shared_task
from app.scanner.engine import ScanEngine
from app.models.tasks import Task
from app.libs.enums import TaskStatus
from datetime import datetime


@shared_task
def execute_scan_task(task_id: int) -> None:
    """执行扫描任务"""
    task = Task.query.get(task_id)
    if not task:
        return
    
    try:
        # 更新任务状态为运行中
        task.status = TaskStatus.RUNNING
        task.start_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        task.save()
        
        # 启动扫描引擎
        engine = ScanEngine(task_id)
        engine.start()
        
        # 更新任务状态为已完成
        task.status = TaskStatus.COMPLETED
        task.end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        task.save()
    except Exception as e:
        # 发生异常时更新任务状态为失败
        task.status = TaskStatus.FAILED
        task.end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        task.save()
        raise e

