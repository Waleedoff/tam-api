
from datetime import datetime

from app.api.auth.schema import UserResponse
from pydantic import BaseModel

from app.api.todos.enums import Priority


class TodoEmpResponse(BaseModel):
    id: str
    title: str
    desription: str
    priority: str
    status: str
    estimate: int
    assign_to: str | None = "waleed ahmad"
    # created_by: str

class TodoResponse(BaseModel):
    
    class KeyResultResponse(BaseModel):
        
        class GoalResponse(BaseModel):
            id: str
            title: str
        
        id: str
        title: str
        goal: GoalResponse        
    
    id: str
    title: str
    desription: str 
    priority: str
    status: str
    key_results: KeyResultResponse
    estimate: int
    created: datetime
    
    class Config:
        form_attribute = True

class TodoCreateRequest(BaseModel):

    title: str
    desription: str
    status: str
    estimate: int
    priority: Priority
    user_story_id: str


class TodoUpdateRequest(BaseModel):
    title: str


class RecentTasks(BaseModel):
    task: str
    status: str

class TaskStatistics(BaseModel):
    pending_count: int
    in_progress: int
    completed: int
    recent_tasks: list[RecentTasks]




class TodoUsersResponse(BaseModel):
    id: str
    title: str
    desription: str | None
    priority: str
    status: str
    created: datetime
    user_info: UserResponse

    class Config:
        form_attribute = True