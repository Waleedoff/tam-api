from datetime import datetime

import sqlalchemy as sa
from sqlalchemy.orm import Mapped

from app.db.db import Base, Defaults


class EmailLog(Base, Defaults):
    source_id = sa.Column(sa.String, nullable=False, index=True)
    source_type = sa.Column(sa.String, nullable=False)
    message_body = sa.Column(sa.String, nullable=False)
    recipient_email = sa.Column(sa.String, nullable=False, index=True)
    subject = sa.Column(sa.String, nullable=False)
    created: Mapped[datetime] = sa.Column(sa.DateTime, default=datetime.now, nullable=False, index=True)  # type: ignore
    updated = None  # type: ignore
    created_by = None  # type: ignore

