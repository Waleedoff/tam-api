from sqlalchemy.orm.session import Session
from sqlalchemy.sql.expression import exists

from app.common.models import EmailLog


def email_has_received_message(email: str, source_id: str, session: Session) -> bool:
    stmt = (
        exists(EmailLog)
        .where(  # type: ignore
            EmailLog.source_id == source_id,
            EmailLog.recipient_email == email,
        )
        .select()
    )  # type: ignore

    return session.execute(stmt).scalar_one()
