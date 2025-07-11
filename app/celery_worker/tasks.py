from app.celery_worker.app import init_app, stop_http_errors
from app.config import config

celery = init_app(config=config)


@celery.task()
def test_task(*args, **kwargs) -> str:
    return "test task is ok"



@celery.task(bind=True)
@stop_http_errors
def send_email_task(*args, **kwargs) -> str:
    from app.celery_worker.send_email_task import send_email_task_

    return send_email_task_(*args, **kwargs)

