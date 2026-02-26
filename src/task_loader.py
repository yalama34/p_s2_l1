from .contract import TaskSource
from .task import Task
from typing import List

class TaskLoader:
    """
    Task loader class
    """
    __slots__ = ("_tasks",)
    def __init__(self):
        self._tasks: List[Task] = []

    def add_source(self, source: TaskSource) -> None:
        """
        Get tasks from source if it's fitting the contract
        :param source:
        :return: None
        """
        if not isinstance(source, TaskSource):
            raise TypeError("Current source does not fit the contract\nmethod get_tasks() did not found")
        source_tasks: List[Task] = source.get_tasks()
        self._tasks.extend(source_tasks)
        print(f"Loader successfully added tasks from source {source.__class__.__name__}")

    def get_tasks(self) -> List[Task]:
        """
        Return all tasks
        :return: copy of tasks
        """
        return self._tasks.copy()

    def clear_tasks(self) -> None:
        """
        Clear all tasks
        :return: None
        """
        self._tasks.clear()
