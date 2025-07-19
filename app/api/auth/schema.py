from app.common.enums import Gender, Department, Role
from pydantic import BaseModel


class CreateUserRequest(BaseModel):
    full_name: str
    username: str
    password: str | None = None
    email: str
    gender: Gender
    department: Department
    role: Role
    


class UserLoginRequest(BaseModel):

    username: str
    password: str



class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None
    department: str | None = None


class UserResponse(BaseModel):
    id: str
    username: str
    email: str | None = None
    full_name: str | None = None
    disabled: bool | None = None
    department: Department
    role: Role


class UserInDB(UserResponse):
    hashed_password: str

class GetMemeberInfoResponse(BaseModel):
    id: str
    username: str
    email: str
    full_name: str
    gender: Gender
    department: Department