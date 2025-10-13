
from datetime import datetime

from pydantic import BaseModel


class CreateSprintRequest(BaseModel):
  
    name: str
    description: str | None
    # priority: str
    status: str
    start_date: datetime
    end_date: datetime

    class Config:
        form_attribute = True


class SprintPreviewResponse(BaseModel):
    id: str
    name: str
    status: str
    # priority: str
    created: datetime
    