from app.celery_worker.app import CustomTask
from app.common.logging import logging


def check_envs(self: CustomTask):
    required_envs_list = ["SMTP_SENDER", "SMTP_SENDERNAME", "SMTP_HOST", "SMTP_PORT"]

    missing_envs = [env_name for env_name in required_envs_list if self.app_config.__getattribute__(env_name) is None]

    for env_name in missing_envs:
        logging.exception(f"please  set {env_name} on app")

    if self.app_config.SMTP_PORT != "587" and self.app_config.ENVIRONMENT == "prod":
        logging.warning(
            f"SMTP_PORT != '587' !! , SMTP_PORT:{self.app_config.SMTP_PORT}"
        )
    return missing_envs
