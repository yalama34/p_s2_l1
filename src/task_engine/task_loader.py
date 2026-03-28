"""Aggregates tasks from multiple sources that satisfy :class:`TaskSource`."""

from typing import List

from .contract import TaskSource
from .task import Task


class TaskLoader:
    """Collects tasks from registered sources at runtime (duck-typed via :class:`TaskSource`)."""

    __slots__ = ("_tasks",)

    def __init__(self) -> None:
        self._tasks: List[Task] = []

    def add_source(self, source: TaskSource) -> None:
        """Append tasks from ``source`` if it implements the protocol; otherwise raise :exc:`TypeError`."""
        if not isinstance(source, TaskSource):
            raise TypeError("Current source does not fit the contract\nmethod get_tasks() did not found")
        source_tasks: List[Task] = source.get_tasks()
        self._tasks.extend(source_tasks)
        print(f"Loader successfully added tasks from source {source.__class__.__name__}")

    def get_tasks(self) -> List[Task]:
        """Return a shallow copy of all loaded tasks."""
        return self._tasks.copy()

    def clear_tasks(self) -> None:
        """Remove every stored task."""
        self._tasks.clear()
