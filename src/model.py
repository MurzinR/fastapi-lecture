import datetime
from enum import Enum
from uuid import UUID

from pydantic import BaseModel


class Task(BaseModel):
    id: UUID
    timeout: float


class TaskStatus(Enum):
    DRAFT = 'DRAFT'
    SENT = 'SENT'
    SOLVING = 'SOLVING'
    SOLVED = 'SOLVED'
    FAILED = 'FAILED'


class TaskTrace(BaseModel):
    task_id: UUID
    ts: datetime.datetime
    status: TaskStatus
    user_message: str
    developer_message: str
