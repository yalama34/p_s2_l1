from .task import Task
from typing import Iterator


class TaskIterator:
    __slots__ = ('_source_factory',)

    def __init__(self, source_factory: Iterator[Task]) -> None:
        self._source_factory = source_factory

    def __iter__(self) -> 'TaskIterator':
        return self

    def __next__(self):
        return next(self._source_factory)



