"""Protocol for pluggable task providers (structural typing)."""

from typing import Protocol, runtime_checkable, Iterator

from src.engine.task import Task


@runtime_checkable
class TaskSource(Protocol):

    def get_tasks(self) -> Iterator[Task]:
        """Return zero or more tasks from this source."""
        ...
