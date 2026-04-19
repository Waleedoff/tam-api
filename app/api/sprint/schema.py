
from datetime import datetime

from pydantic import BaseModel


class CreateSprintRequest(BaseModel):
    
    class UserStoryRequest(BaseModel):
        id: str
        title: str
        descritpion: str

    name: str
    description: str | None
    # priority: str
    start_date: datetime
    end_date: datetime
    user_stories: list[UserStoryRequest]

    class Config:
        form_attribute = True


class SprintPreviewResponse(BaseModel):
       
    class UserStoryRequest(BaseModel):
        id: str
        title: str
        story_points: int
        status: str
        theStory: dict
    id: str
    name: str
    description: str | None
    status: str
    # priority: str
    user_stories: list[UserStoryRequest]
    


from datetime import datetime


class SprintOverviewItem(BaseModel):
    id: str
    name: str
    description: str | None = None
    start_date: datetime
    end_date: datetime

    total_stories: int
    completed_stories: int

    total_points: int
    completed_points: int

    progress_percentage: int

    class Config:
        from_attributes = True


class SprintOverviewResponse(BaseModel):
    planned: list[SprintOverviewItem]
    completed: list[SprintOverviewItem]