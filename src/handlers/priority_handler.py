import asyncio
import logging

from ..engine.task import Task

logger = logging.getLogger(__name__)

class PriorityHandler:
    async def handle(self, task: Task) -> None:
        await asyncio.to_thread(task.change_status)
        await asyncio.sleep(task.priority * 0.1)
        logger.info(f"Task {task.id} handled successfully.")
        await asyncio.to_thread(task.change_status)


