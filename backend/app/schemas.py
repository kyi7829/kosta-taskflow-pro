from datetime import datetime
from typing import Literal, Optional
from pydantic import BaseModel, Field


class TaskCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = None
    status: Literal["todo", "in_progress", "done"] = "todo"
    due_at: Optional[datetime] = None


class TaskUpdate(BaseModel):
    title: Optional[str] = Field(default=None, min_length=1, max_length=200)
    description: Optional[str] = None
    status: Optional[Literal["todo", "in_progress", "done"]] = None
    due_at: Optional[datetime] = None


class TaskSummary(BaseModel):
    """목록 조회용 — description 제외"""
    id: int
    title: str
    status: str
    due_at: Optional[datetime]
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class TaskDetail(BaseModel):
    """단건 조회용 — description 포함"""
    id: int
    title: str
    description: Optional[str]
    status: str
    due_at: Optional[datetime]
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
