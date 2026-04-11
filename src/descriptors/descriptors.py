from __future__ import annotations


from datetime import datetime
from typing import TYPE_CHECKING, Any

from ..engine.task_errors import InvalidCreationDateError, InvalidPriorityError, InvalidStatusError
from ..engine.enums import TaskStatus


if TYPE_CHECKING:
    from ..engine.task import Task


class PriorityDescriptor:
    """Validate ``priority`` parameter. It must be an integer in range between ``0`` and ``5``."""

    def __set_name__(self, owner: Task, name: str) -> None:
        self.name: str = "_" + name

    def __get__(self, obj: Task, obj_type=None) -> Any:
        if obj is None:
            return self

        return getattr(obj, self.name, None)

    def __set__(self, obj: Task, value: int) -> None:
        if not isinstance(value, int) or not 0 <= value <= 5:
            raise InvalidPriorityError(value)

        setattr(obj, self.name, value)

    def __delete__(self, obj: Task) -> None:
        delattr(obj, self.name)


class CreatedAtDescriptor:
    """Validate ``created_at`` parameter. It must be a datetime object, not later than ``datetime.now()`` """

    def __set_name__(self, owner: Task, name: str) -> None:
        self.name = "_" + name

    def __get__(self, obj: Task, obj_type=None) -> Any:
        if obj is None:
            return self

        return getattr(obj, self.name, None)

    def __set__(self, obj: Task, value: datetime) -> None:
        if not isinstance(value, datetime):
            raise InvalidCreationDateError(value)
        now = datetime.now(value.tzinfo) if value.tzinfo else datetime.now()
        if value > now:
            raise InvalidCreationDateError(value)

        setattr(obj, self.name, value)

    def __delete__(self, obj) -> None:
        delattr(obj, self.name)


class StatusDescriptor:
    """Validate status parameter. It must be a string from ``valid_statuses``: ``"new", "in_progress", "done", "cancelled"`` """

    valid_statuses = [status.name for status in TaskStatus]

    def __set_name__(self, owner: Task, name: str) -> None:
        self.name = "_" + name

    def __get__(self, obj: Task, obj_type=None) -> Any:
        if obj is None:
            return self
        return getattr(obj, self.name, None)

    def __set__(self, obj: Task, value: TaskStatus) -> None:
        if not isinstance(value, TaskStatus):
            raise InvalidStatusError(
                f"Status must be TaskStatus enum, got {type(value).__name__}: {value}"
            )
        setattr(obj, self.name, value)

    def __delete__(self, obj) -> None:
        delattr(obj, self.name)

class IsReadyDescriptor:
    def __get__(self, obj: Task, obj_type=None) -> Any:
        if obj is None:
            return self
        return obj.priority == 5 and obj.status == "new"