from datetime import datetime
from pydantic import BaseModel
from typing import List

from app.api.announcement.enums import AnnouncementStatus
from app.common.enums import Department, Role

class CreateAnnoucementRequest(BaseModel):
    content: str
    title: str
    media_url: str
    target_departments: List[Department]
    target_roles: List[Role]
    publishing_status: AnnouncementStatus
    

    

class CreateAnnoucementResponse(BaseModel):

    class VoteResponse(BaseModel):
        helpfull: int
        unhelpfull: int
    id: str
    content: str
    title: str
    media_url: str
    vote: VoteResponse
    


class CreateAnnouncementComment(BaseModel):
    content: str
    
    
class GetAllAnnouncementComment(BaseModel):
    content: str
    created: datetime
    username: str