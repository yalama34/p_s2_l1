from typing import Callable, Iterator


from .task import Task
from .iterator import TaskIterator


class TaskQueue:
    def __init__(self, task_source_factory: Callable[[], Iterator[Task]]) -> None:
        self._source_factory = task_source_factory

    def __iter__(self):
        return TaskIterator(self._source_factory())

    def filter(self, mask: Callable[[Task], bool]):
        """
        Filter tasks according to the given mask.
        :param mask:
        :return:
        """
        if not callable(mask):
            raise TypeError('Mask must be callable')

        for task in self:
            if mask(task):
                yield task
