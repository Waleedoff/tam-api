import smtplib
from email.mime.multipart import MIMEMultipart

from app.celery_worker.app import CustomTask


def send_email(
    self: CustomTask,
    user_email: str,
    message: MIMEMultipart,
):
    assert self.app_config.SMTP_HOST is not None, "SMTP_HOST is not set!"
    assert self.app_config.SMTP_PORT is not None, "SMTP_PORT is not set!"
    server = smtplib.SMTP(self.app_config.SMTP_HOST, self.app_config.SMTP_PORT, timeout=self.app_config.SMTP_TIMEOUT)
    server.ehlo()
    if self.app_config.SMTP_ENCRYPTION:
        server.starttls()
    server.ehlo()
    username = self.app_config.SMTP_USERNAME
    password = self.app_config.SMTP_PASSWORD
    if username is not None and password is not None:
        server.login(username, password)
    server.sendmail(self.app_config.SMTP_SENDER, user_email, message.as_string())
    server.close()
