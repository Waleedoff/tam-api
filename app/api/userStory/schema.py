from app.api.room.enums import WorkItemType
from app.api.todos.enums import Priority
from app.api.userStory.enums import ActorType, PipelineStage, UserStoryStatus
from pydantic import BaseModel, field_validator
from datetime import datetime
from typing import Optional, Any, Dict


from pydantic import BaseModel
from typing import Optional


class CreateUserStoryRequest(BaseModel):
    title: str

    # # اختياري لو تحب صيغة "As a ..."
    # actor: Optional[ActorType] = None
    # actor_custom: Optional[str] = None

    # خاص بالـStory
    acceptance_criteria: Optional[str] = None
    story_points: Optional[int] = None

    # ميتاداتا الباكلوغ
    # work_item_type: WorkItemType = WorkItemType.STORY
    priority: Priority = Priority.MEDIUM
    # pipeline_stage: PipelineStage = PipelineStage.IDEA
    order_rank: Optional[float] = None  # لو ما انرسلت بنحسبها تلقائيًا

    # للـBug/Spike.. إلخ (حقول مرنة)
    theStory: Optional[Dict[str, Any]] = None
    backlog_id: str
    # الجدولة اختيارية
    sprint_id: Optional[str] = None

    # @field_validator('actor_custom')
    # def _actor_custom_if_other(cls, v, info):
    #     actor = info.data.get("actor")
    #     if actor == ActorType.OTHER and not v:
    #         raise ValueError("actor_custom مطلوب عندما actor=other")
    #     return v

    # @field_validator('acceptance_criteria')
    # def _ac_required_for_story(cls, v, info):
    #     if info.data.get("work_item_type") == WorkItemType.STORY and not v:
    #         raise ValueError("acceptance_criteria مطلوبة للـStory")
    #     return v

    # @field_validator('extras')
    # def _extras_required_for_bug(cls, v, info):
    #     if info.data.get("work_item_type") == WorkItemType.BUG:
    #         if not isinstance(v, dict):
    #             raise ValueError("extras مطلوبة للـBug")
    #         required = ["severity","repro_steps","expected","actual","environment"]
    #         missing = [k for k in required if k not in v]
    #         if missing:
    #             raise ValueError(f"extras للـBug ناقصة: {missing}")
    #     return v

# ✅ Create Response Schema
class CreateUserStoryResponse(BaseModel):
    id: str
    title: Optional[str] = None
    description: Optional[str] = None


    acceptance_criteria: Optional[str] = None

    priority: str
    status: str
    story_points: Optional[int] = None
    the_story: Optional[Dict[str, Any]] = None
    # backlog_title: str

    class Config:
        from_attributes = True
