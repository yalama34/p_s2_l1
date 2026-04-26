from typing import Protocol, runtime_checkable
from ..engine.task import Task


@runtime_checkable
class TaskHandler(Protocol):
    async def handle(self, task: Task):
        ...