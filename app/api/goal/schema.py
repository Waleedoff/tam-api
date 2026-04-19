
from datetime import datetime

from pydantic import BaseModel


class CreateGoalReques(BaseModel):
    class CreateKeyResult(BaseModel):
        title: str
        target_value: float
    title: str
    description: str
    deadline: datetime
    key_results: list[CreateKeyResult] 
    
    class Config:
        form_attribute = True

    


class GoalResponse(BaseModel):
    id: str
    title: str
    description: str
    # key_results: list[dict]
    class Config:
        form_attribute = True



class CreateGoalResponse(BaseModel):
    class CreateKeyResult(BaseModel):
        id: str
        title: str
        target_value: float
    id: str
    title: str
    description: str
    deadline: datetime
    key_results: list[CreateKeyResult] 
    
    class Config:
        from_attributes = True

    


class GoalResponse(BaseModel):
    id: str
    title: str
    description: str
    # key_results: list[dict]
    class Config:
        form_attribute = True