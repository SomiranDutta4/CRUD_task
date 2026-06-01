from pydantic import BaseModel, EmailStr
from typing import Optional


class AdminSignUp(BaseModel):
    username: str
    email: EmailStr
    password: str
    admin_key: str

class AdminSignin(BaseModel):
    email:EmailStr
    password:str
    admin_key:str


class AdminResponse(BaseModel):
    id: str
    username: str
    email: EmailStr
    isAdmin: bool


class ManagerUpdateSchema(BaseModel):
    employee_id: str
    manager_id: str