from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional


# ── User Schemas ──────────────────────────
class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str


class UserOut(BaseModel):
    id: int
    username: str
    email: str


class Config:
    from_attributes = True


# ── Task Schemas ──────────────────────────
class TaskCreate(BaseModel):
    title: str
    description: Optional[str] = None 
    deadline: Optional[datetime] = None


class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    deadline: Optional[datetime] = None
    is_done: Optional[bool] = None


class TaskOut(BaseModel):
    id: int
    title: str
    description: Optional[str]
    deadline: Optional[datetime]
    is_done: bool
    created_at: datetime


class Config:
    from_attributes = True


# ── Token Schema ──────────────────────────
class Token(BaseModel):
    access_token: str
    token_type: str