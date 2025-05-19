
from sqlalchemy import Column, Integer, String, Text, Date, ForeignKey, DateTime
from enum import Enum  
from sqlalchemy import Enum as SQLEnum  
from sqlalchemy.sql import func
from sqlalchemy.ext.declarative import declarative_base
from .db import engine


Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)
    created_at = Column(DateTime, server_default=func.now())

class TaskStatus(str, Enum):
    pending = "pending"
    completed = "completed"

class TaskPriority(str, Enum):
    low = "low"
    medium = "medium"
    high = "high"

class Task(Base):
    __tablename__ = "tasks"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    title = Column(String, nullable=False)
    description = Column(Text)
    due_date = Column(Date, nullable=False)
    status = Column(SQLEnum(TaskStatus), default=TaskStatus.pending)
    priority = Column(SQLEnum(TaskPriority), default=TaskPriority.medium)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())

Base.metadata.create_all(engine)

