from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List
from .model import TaskPriority, TaskStatus

class TaskBase(BaseModel):
    title: str
    description: Optional[str] = None
    priority: Optional[TaskPriority] = None  # Default priority

class TaskCreate(TaskBase):
    pass

class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    priority: Optional[TaskPriority] = None
    status: Optional[TaskStatus] = None  # Status can be updated

class TaskResponse(TaskBase):
    id: int
    status: TaskStatus
    created_at: datetime
    

    class Config:
        from_attributes = True

class PaginatedTaskResponse(BaseModel):
    items: List[TaskResponse]
    total: int
    page: int
    pages: int
    size: int
    
    class Config:
        from_attributes = True