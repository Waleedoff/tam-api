import email.utils
from datetime import datetime
from email.message import Message
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from app.celery_worker.app import CustomTask


def make_message(
    self: CustomTask,
    subject: str,
    user_email: str,
    html_body: str,
    extra_attachments: list[Message] = [],
):
    message = MIMEMultipart("alternative")
    message["Subject"] = subject
    message["From"] = email.utils.formataddr((self.app_config.SMTP_SENDERNAME, self.app_config.SMTP_SENDER))
    message["To"] = user_email

    now_date = datetime.now().strftime("%d/%m/%Y %I:%M:%S %p").replace("PM", "مساء").replace("AM", "صباحا")
    html_body = html_body.replace("{{now_date}}", now_date)

    message.attach(MIMEText(html_body, "html"))

    for attachment in extra_attachments:
        message.attach(attachment)

    return message
