
from datetime import datetime
from app.api.userStory.enums import PipelineStage
import sqlalchemy as sa
from sqlalchemy.orm import Mapped, relationship

from app.api.todos.enums import Priority
from app.db.db import Base, Defaults
from app.api.room.enums import  Methdology, ProjectStatus, RoomMemberRole, RoomMemberStatus, Visibility, WorkItemType





class Room(Base, Defaults):
    name: Mapped[str] = sa.Column(sa.String, nullable=False)  # type: ignore
    description: Mapped[str] = sa.Column(sa.String, nullable=False) # type: ignore
    priority: Mapped[str] = sa.Column(sa.String, nullable=False, default=Priority.LOW) # type: ignore
    status: Mapped[str] = sa.Column(sa.String, nullable=False, default=ProjectStatus.DRAFT)  # type: ignore
    sprint_length_days: Mapped[int] = sa.Column(sa.Integer, nullable=False)
    visibility: Mapped[str] = sa.Column(sa.String, nullable=False, default=Visibility.PUBLIC)
    methodology: Mapped[str] = sa.Column(sa.String, nullable=False, default=Methdology.SCRUM)
    user_id: Mapped[str] = sa.Column(sa.String, sa.ForeignKey('auth_user.id'), nullable=False)  # type: ignore
    user = relationship("User", back_populates="rooms", foreign_keys=[user_id])
    tasks = relationship("Todo", back_populates="room")  # ← داخل Room   
    # في model Room
    
    messages = relationship("Message", back_populates="room", cascade="all, delete-orphan")
    
    # product owner
    product_owner_id:  Mapped[str] = sa.Column(sa.String, sa.ForeignKey('auth_user.id'))
    product_owner = relationship("User", backref="owned_projects", foreign_keys=[product_owner_id])
    sprints = relationship("Sprint", back_populates="room", cascade="all, delete-orphan")
    user_stories = relationship("UserStory", back_populates="room", cascade="all, delete-orphan")


    members_assoc = relationship("RoomMember", back_populates="room", cascade="all, delete-orphan")
    users = relationship(
        "User",
        secondary="room_members",
        primaryjoin="Room.id==RoomMember.room_id",
        secondaryjoin="User.id==RoomMember.user_id",
        viewonly=True
    )

class RoomMember(Base, Defaults):
    __tablename__ = "room_members"

    # المفتاح المركّب: كل مستخدم مرة واحدة لكل مشروع
    room_id: Mapped[str] = sa.Column(
        sa.String, sa.ForeignKey("rooms.id", ondelete="CASCADE"),
        primary_key=True
    )
    user_id: Mapped[str] = sa.Column(
        sa.String, sa.ForeignKey("auth_user.id", ondelete="CASCADE"),
        primary_key=True
    )

    # دور العضو داخل هذا المشروع فقط
    role_in_room: Mapped[RoomMemberRole] = sa.Column(
        sa.Enum(RoomMemberRole), nullable=False, default=RoomMemberRole.MEMBER
    )

    # سِعة العضو لهذا المشروع (اختياري)
    capacity_hours_per_week: Mapped[int | None] = sa.Column(sa.Integer, nullable=True)

    # مهارات العضو لهذا المشروع (اختياري) — مثال: ["frontend","backend","qa"]
    skills: Mapped[dict | None] = sa.Column(sa.JSON, nullable=True)

    # حالة العضوية
    status: Mapped[RoomMemberStatus] = sa.Column(
        sa.Enum(RoomMemberStatus), nullable=False, default=RoomMemberStatus.ACTIVE
    )

    joined_at: Mapped[datetime] = sa.Column(
        sa.DateTime, nullable=False, server_default=sa.func.now()
    )

    # علاقات
    room = relationship("Room", back_populates="members_assoc")
    user = relationship("User", back_populates="memberships")

    __table_args__ = (
        sa.Index("ix_room_members_status", "room_id", "status"),
    )
    

class Sprint(Base, Defaults):
    # اسم السبرنت
    name: Mapped[str] = sa.Column(sa.String, nullable=False)  # مثل: Sprint 1
    # وصف السبرنت
    description: Mapped[str] = sa.Column(sa.Text, nullable=True)
    # تاريخ البداية والنهاية
    start_date: Mapped[datetime] = sa.Column(sa.DateTime, nullable=False)
    end_date: Mapped[datetime] = sa.Column(sa.DateTime, nullable=False)
    # حالة السبرنت (مفتوح - مغلق - مؤجل)
    status: Mapped[str] = sa.Column(sa.String, nullable=False, default="PLANNED")  
    # ممكن تستخدم Enum إذا تحب
    # ربط السبرنت بالمشروع (Room)
    room_id: Mapped[str] = sa.Column(sa.String, sa.ForeignKey("rooms.id", ondelete="CASCADE"),  nullable=False)
    room = relationship("Room", back_populates="sprints")
    # ربط المهام بالسبرنت
    tasks = relationship("Todo", back_populates="sprint", cascade="all, delete-orphan")
    user_stories = relationship("UserStory", back_populates="sprint", cascade="all, delete-orphan")
    
    __table_args__ = (sa.CheckConstraint("end_date > start_date", name="ck_sprint_dates"),)



# TODO: SHOULD CHANGE USERSTORY NAME TO WORK_ITEM.

# TODO should add visibility column to conform if allowed to be public could
# every one has access on backlog see it or just to make it belong to you never seen by others.

class UserStory(Base, Defaults):
    __tablename__ = "user_stories"    
    
    # العنوان والوصف
    title: Mapped[str] = sa.Column(sa.String, nullable=False)  # type: ignore
    description: Mapped[str] = sa.Column(sa.Text, nullable=True)  # type: ignore
    # نوع المستخدم (As a ...)
    actor: Mapped[str] = sa.Column(sa.String, nullable=False, default="user")  # type: ignore
    actor_custom: Mapped[str] = sa.Column(sa.String, nullable=True)  # type: ignore
    # معايير القبول (BDD format)
    acceptance_criteria: Mapped[str] = sa.Column(sa.Text, nullable=True)  # type: ignore
    order_rank = sa.Column(sa.Numeric(18,6), nullable=False, default=1000)  # type: ignore
    
    # الأولوية، الحالة، التقدير
    priority: Mapped[str] = sa.Column(sa.String, nullable=False, default="medium")  # type: ignore
    status: Mapped[str] = sa.Column(sa.String, nullable=False, default="not_started")  # type: ignore
    story_points: Mapped[int] = sa.Column(sa.Integer, nullable=True)  # type: ignore
    pipeline_stage: Mapped[str] = sa.Column(sa.String, nullable=False, default=PipelineStage.IDEA) # type: ignore
    work_item_type: Mapped[str] = sa.Column(sa.String, nullable=False, default=WorkItemType.STORY) # type: ignore
    extras = sa.Column(sa.JSON, nullable=True)
   
    # العلاقة مع Sprint
    sprint_id: Mapped[str] = sa.Column(sa.String, sa.ForeignKey("sprints.id"), nullable=True)  # type: ignore
    sprint = relationship("Sprint", back_populates="user_stories")
    room_id: Mapped[str] = sa.Column(sa.String, sa.ForeignKey("rooms.id", ondelete="CASCADE"), nullable=False)
    room = relationship("Room", back_populates="user_stories")
    # العلاقة مع المهام
    tasks = relationship("Todo", back_populates="user_story", cascade="all, delete-orphan")
    
    