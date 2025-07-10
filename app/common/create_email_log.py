from app.celery_worker.app import CustomTask
from app.common.logging import logging
from app.common.models import EmailLog


def create_email_log(
    self: CustomTask,
    recipient_email: str,
    subject: str,
    source_id: str,
    source_type: str,
    email_body: str,
):
    try:
        email = EmailLog(
            recipient_email=recipient_email,
            subject=subject,
            source_id=source_id,
            source_type=source_type,
            message_body=email_body,
        )
        with self.session.begin_nested():
            self.session.add(email)

    except Exception as exception:
        logging.exception(exception)
        return None
