from __future__ import annotations

"""Domain model for a single processing task."""

from datetime import datetime
from typing import Optional

from ..descriptors.descriptors import PriorityDescriptor, StatusDescriptor, CreatedAtDescriptor, IsReadyDescriptor


class Task:
    """Task with validated priority, status, and creation time.

    ``id`` and ``description`` are exposed via the builtin ``property`` (getter/setter/deleter);
    ``priority``, ``status``, ``created_at``, and ``is_ready`` use custom descriptors.
    """

    __slots__ = ('_id', '_description', '_priority', '_status', '_created_at')

    priority = PriorityDescriptor()
    status = StatusDescriptor()
    created_at = CreatedAtDescriptor()
    is_ready = IsReadyDescriptor()

    def __init__(
        self,
        id: int,
        description: str,
        priority: int,
        status: str = "new",
        created_at: Optional[datetime] = None,
    ) -> None:
        """Create a task. If ``created_at`` is omitted, the current time is used."""
        self.id = id
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
    def id(self) -> int:
        return self._id

    @id.setter
    def id(self, value: int) -> None:
        if not isinstance(value, int) or value < 0:
            raise ValueError("ID must be a non-negative integer")
        self._id = value

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

