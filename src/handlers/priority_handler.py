import asyncio
import logging

from ..engine.task import Task

logger = logging.getLogger(__name__)

class PriorityHandler:
    async def handle(self, task: Task) -> None:
        task.change_status()
        await asyncio.sleep(task.priority * 0.1)
        logger.info(f"Task {task.id} handled successfully.")
        task.change_status()


