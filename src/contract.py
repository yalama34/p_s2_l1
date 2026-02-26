from typing import Protocol, runtime_checkable, List
from .task import Task

@runtime_checkable
class TaskSource(Protocol):
    def get_tasks(self) -> List[Task]:
        """
        :return: list of tasks
        """
        ...

