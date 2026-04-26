import logging
import random

from ..engine.task import Task
from ..engine.task_errors import TaskError


logger = logging.getLogger(__name__)


class RandomHandler:
    def __init__(self, seed: int) -> None:
        self._seed = seed
        random.seed(self._seed)

    async def handle(self, task: Task) -> None:
        task.change_status()
        if random.random() < 0.2:
            logger.warning(f"Simulating failure for task {task.id}")
            task.failure()
            raise TaskError(f"Task {task.id} failed")
        else:
            logger.info(f"Task {task.id} handled successfully.")
            task.change_status()