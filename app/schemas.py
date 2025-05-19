from pydantic import BaseModel
from datetime import datetime, date
from typing import Optional
from .models import TaskPriority, TaskStatus

class UserCreate(BaseModel):
    name: str
    email: str
    password: str

class UserLogin(BaseModel):
    email: str
    password: str

class UserResponse(BaseModel):
    id: int
    name: str
    email: str
    created_at: datetime

class Token(BaseModel):
    access_token: str
    token_type: str

class TaskBase(BaseModel):
    title: str
    description: Optional[str] = None
    due_date: date
    priority: TaskPriority = TaskPriority.medium

class TaskCreate(TaskBase):
    pass

class TaskResponse(TaskBase):
    id: int
    status: TaskStatus
    user_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    due_date: Optional[date] = None
    status: Optional[TaskStatus] = None
    priority: Optional[TaskPriority] = None