from celery import shared_task


@shared_task
def send_scanner_tasks(target_url: str = 'http://www.example.com.cn') -> dict:
    return {'id': 'xxx', 'url': target_url}

