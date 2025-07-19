
import sqlalchemy as sa
from sqlalchemy.orm import Mapped, relationship

from app.db.db import Base, Defaults
from app.api.organization.enums import SubscriptionPan

class Organization(Base, Defaults):

    name: Mapped[str] = sa.Column(sa.String, nullable=False)  # type: ignore
    industry: Mapped[str] = sa.Column(sa.String, nullable=False)  # type: ignore
    subscription_plan: Mapped[str] = sa.Column(sa.String, nullable=False, default=SubscriptionPan.STARTUP.value)  # type: ignore
    is_active: Mapped[bool] = sa.Column(sa.Boolean, nullable=False, default=False)  # type: ignore
    users = relationship("User", back_populates="organization") # check if back_populates related to variable in another model.
    announcements = relationship("Announcement", back_populates="organization")
