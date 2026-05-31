from __future__ import annotations
from dataclasses import dataclass

@dataclass(slots=True)
class MemoryItem:
    id: int
    kind: str
    key: str
    value: str
    tags: str
    source: str
    created_at: str
    updated_at: str

@dataclass(slots=True)
class TaskItem:
    id: int
    title: str
    description: str
    status: str
    due_at: str | None

@dataclass(slots=True)
class ReminderItem:
    id: int
    title: str
    remind_at: str
    status: str
