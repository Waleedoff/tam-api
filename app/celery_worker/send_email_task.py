import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import formataddr

from app.celery_worker.app import CustomTask
from app.common.assets_reader import AssetsReader
from app.common.check_envs import check_envs
from app.common.create_email_log import create_email_log
from app.common.email_has_received_message import email_has_received_message
from app.common.fill_placeholders import fill_placeholders
from app.common.logging import logging


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
        # TODO replace source_id to otp
        if "OTP" in source_id:
            pass
        else:
            logging.exception("received email that already received message")
            return None

    pure_email_template = AssetsReader.read_email_template(template_name=email_template)

    final_html_body = fill_placeholders(
        data_to_be_filled=data_to_be_filled, html_body=pure_email_template
    )

    missing_envs = check_envs(self)

    if len(missing_envs) > 0:
        return f"missing required envs! , missing_envs:{missing_envs}"

    message = MIMEMultipart("alternative")
    message["Subject"] = subject
    message["From"] = formataddr(
        (self.app_config.SMTP_SENDERNAME, self.app_config.SMTP_SENDER)
    )
    message["To"] = user_email
    message.attach(MIMEText(final_html_body, "html"))

    assert self.app_config.SMTP_HOST is not None, "SMTP_HOST is not set!"
    assert self.app_config.SMTP_PORT is not None, "SMTP_PORT is not set!"

    server = smtplib.SMTP(
        self.app_config.SMTP_HOST,
        self.app_config.SMTP_PORT,
        timeout=self.app_config.SMTP_TIMEOUT,
    )

    server.ehlo()

    if self.app_config.SMTP_ENCRYPTION:
        server.starttls()

    server.ehlo()

    username = self.app_config.SMTP_USERNAME
    password = self.app_config.SMTP_PASSWORD

    if username is not None and password is not None:
        server.login(username, password)

    try:
        server.sendmail(self.app_config.SMTP_SENDER, user_email, message.as_string())
    except smtplib.SMTPDataError as e:

        logging.exception(e, exc_info=e, stack_info=True)
        # throttling failure!
        self.retry(countdown=60)

    create_email_log(
        self,
        recipient_email=user_email,
        subject=subject,
        source_id=source_id,
        source_type=source_type,
        email_body=final_html_body,
    )

    try:
        server.close()
        return f"email is sent to {user_email}"
    except Exception as e:
        logging.exception(e)
        return f"failed to close server connection after sending email to {user_email}"
