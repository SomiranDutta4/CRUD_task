from pydantic import BaseModel, EmailStr
from typing import Optional

class UserSignup(BaseModel):
    username: str
    email: EmailStr
    password: str


class UserSignin(BaseModel):
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    id:str
    username: str
    email: EmailStr
    isAdmin: bool=False

    class Config:
        from_attributes = True
