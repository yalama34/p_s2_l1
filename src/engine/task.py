from __future__ import annotations
from datetime import datetime
from typing import Optional
from uuid import uuid4, UUID

from ..descriptors.descriptors import PriorityDescriptor, StatusDescriptor, CreatedAtDescriptor, IsReadyDescriptor
from .enums import TaskStatus


class Task:
    """Task with validated priority, status, and creation time.

    ``id`` is a read-only :class:``uuid.UUID`` assigned at construction;
    ``description`` uses the builtin ``property`` (getter/setter/deleter);
    ``priority``, ``status``, ``created_at``, and ``is_ready`` use custom descriptors.
    """

    __slots__ = ('_id', '_description', '_priority', '_status', '_created_at')

    priority = PriorityDescriptor()
    status = StatusDescriptor()
    created_at = CreatedAtDescriptor()
    is_ready = IsReadyDescriptor()

    def __init__(
        self,
        description: str,
        priority: int,
        status: TaskStatus = TaskStatus.NEW,
        created_at: Optional[datetime] = None,
    ) -> None:
        """Create a task with a new random id. If ``created_at`` is omitted, the current time is used."""
        object.__setattr__(self, "_id", uuid4())
        self.description = description
        self.priority = priority
        self.status = status
        if created_at is None:
            created_at = datetime.now()
        self.created_at = created_at

    def __repr__(self) -> str:
        return (
            f"Task(id={self.id!r}, description={self.description!r}, "
            f"priority={self.priority!r}, status={self.status!r}, created_at={self.created_at!r}), is_ready={self.is_ready!r})"
        )

    @property
    def id(self) -> UUID:
        return self._id

    @id.deleter
    def id(self) -> None:
        del self._id

    @property
    def description(self) -> str:
        return self._description

    @description.setter
    def description(self, value: str) -> None:
        if not isinstance(value, str):
            raise ValueError("Description must be a string")
        self._description = value

    @description.deleter
    def description(self) -> None:
        del self._description

    def change_status(self) -> None:
        """Change the status of the task."""
        self.status = TaskStatus.get_next_status(self.status)

