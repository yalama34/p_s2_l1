import logging
import random
import asyncio

from ..engine.task import Task
from ..engine.task_errors import TaskError


logger = logging.getLogger(__name__)


class RandomHandler:
    def __init__(self, seed: int) -> None:
        self._seed = seed
        random.seed(self._seed)

    async def handle(self, task: Task) -> None:
        await asyncio.to_thread(task.change_status)
        chance = await asyncio.to_thread(random.random)
        logger.info(f"Task {task.id} handled successfully.")
        if chance < 0.2:
            logger.warning(f"Simulating failure for task {task.id}")
            await asyncio.to_thread(task.failure)
            raise TaskError(f"Task {task.id} failed")
        else:
            logger.info(f"Task {task.id} handled successfully.")
            await asyncio.to_thread(task.change_status)