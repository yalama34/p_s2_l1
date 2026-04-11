from typing import List, Iterator


from src.contracts.contract import TaskSource
from .task import Task


class TaskLoader:
    """Collects tasks from registered sources at runtime (duck-typed via :class:`TaskSource`)."""

    __slots__ = ("_sources",)

    def __init__(self) -> None:
        self._sources: List[TaskSource] = []

    def add_source(self, source: TaskSource) -> None:
        """Append tasks from ``source`` if it implements the protocol; otherwise raise :exc:`TypeError`."""
        if not isinstance(source, TaskSource):
            raise TypeError("Current source does not fit the contract\nmethod get_tasks() did not found")

        self._sources.append(source)
        print(f"Loader successfully added tasks from source {source.__class__.__name__}")

        return None

    def get_tasks(self) -> Iterator[Task]:
        """Return a shallow copy of all loaded tasks."""
        for source in self._sources:
            yield from source.get_tasks()
