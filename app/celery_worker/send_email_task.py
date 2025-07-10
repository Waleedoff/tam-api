from app.celery_worker.app import CustomTask
from app.common.assets_reader import AssetsReader
from app.common.check_envs import check_envs
from app.common.create_email_log import create_email_log
from app.common.email_has_received_message import email_has_received_message
from app.common.fill_placeholders import fill_placeholders
from app.common.logging import logging
from app.common.make_message import make_message
from app.common.send_email import send_email


def send_email_task_(
    self: CustomTask,
    source_id: str,
    source_type: str,
    user_email: str,
    subject: str,
    data_to_be_filled: dict,
    email_template: str,
):
    if email_has_received_message(
        email=user_email,
        source_id=source_id,
        session=self.read_only_session,
    ):
        logging.exception("received email that already received message")
        return None

    html_body = fill_placeholders(
        data_to_be_filled=data_to_be_filled,
        html_body=AssetsReader.read_email_template(template_name=email_template),
    )

    missing_envs = check_envs(self)
    if len(missing_envs) > 0:
        return f"we have missing required_envs! , missing_envs:{missing_envs}"

    message = make_message(
        self=self,
        subject=subject,
        user_email=user_email,
        html_body=html_body,
    )

    send_email(self=self, user_email=user_email, message=message)

    create_email_log(
        self,
        source_id=source_id,
        source_type=source_type,
        subject=subject,
        email_body=html_body,
        recipient_email=user_email,
    )

    return f"email is sent to {user_email}"
