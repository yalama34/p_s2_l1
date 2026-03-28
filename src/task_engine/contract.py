"""Protocol for pluggable task providers (structural typing)."""

from typing import List, Protocol, runtime_checkable

from .task import Task


@runtime_checkable
class TaskSource(Protocol):

    def get_tasks(self) -> List[Task]:
        """Return zero or more tasks from this source."""
        ...
