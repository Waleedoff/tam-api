import sqlalchemy as sa
from sqlalchemy.orm import Mapped, relationship
from datetime import datetime
from sqlalchemy import Enum, ForeignKey, UniqueConstraint

from app.common.generate_random_id_uuid import generate_random_id
from app.db.db import Base, Defaults
from app.api.announcement.enums import AnnouncementStatus, VoteType


class Announcement(Base, Defaults):
    __tablename__ = "announcements"

    title: Mapped[str] = sa.Column(sa.String, nullable=False)
    content: Mapped[str] = sa.Column(sa.Text, nullable=False)
    media_url: Mapped[str] = sa.Column(sa.String, nullable=True)

    target_departments: Mapped[list[str]] = sa.Column(sa.ARRAY(sa.String), nullable=False)
    target_roles: Mapped[list[str]] = sa.Column(sa.ARRAY(sa.String), nullable=False)

    publish_at: Mapped[datetime] = sa.Column(sa.TIMESTAMP(timezone=True), nullable=True)
    publishing_status: Mapped[str] = sa.Column(
        sa.Enum(AnnouncementStatus), nullable=False, default=AnnouncementStatus.DRAFT.value
    )
    is_deleted: Mapped[bool] = sa.Column(sa.Boolean, nullable=False, default=False)

    organization_id: Mapped[str] = sa.Column(sa.String, sa.ForeignKey("organizations.id"), nullable=False)
    organization = relationship("Organization", back_populates="announcements")

    # One-to-many: Announcement has many votes
    votes = relationship("AnnouncementVote", back_populates="announcement", cascade="all, delete-orphan")
    
    # في Announcement
    comments = relationship("AnnouncementComment", back_populates="announcement", cascade="all, delete-orphan")


class AnnouncementVote(Base, Defaults):
    __tablename__ = "announcement_votes"

    user_id: Mapped[str] = sa.Column(sa.String, sa.ForeignKey("auth_user.id"), nullable=False) # TODO check i guess we don't needed that.
    announcement_id: Mapped[str] = sa.Column(sa.String, sa.ForeignKey("announcements.id"), nullable=False)
    vote_type: Mapped[str] = sa.Column(sa.Enum(VoteType), nullable=False)

    user = relationship("User", back_populates="announcement_vote")
    announcement = relationship("Announcement", back_populates="votes")
    
    __table_args__ = (
        UniqueConstraint("user_id", "announcement_id", name="unique_user_vote"),
    )


class AnnouncementComment(Base, Defaults):
    __tablename__ = "announcement_comments"
    
    content: Mapped[str] = sa.Column(sa.Text, nullable=False)

    user_id: Mapped[str] = sa.Column(sa.String, sa.ForeignKey("auth_user.id"), nullable=False)
    announcement_id: Mapped[str] = sa.Column(sa.String, sa.ForeignKey("announcements.id"), nullable=False)

    user = relationship("User", back_populates="announcement_comments")
    announcement = relationship("Announcement", back_populates="comments")
