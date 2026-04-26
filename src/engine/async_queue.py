import asyncio
import logging

from .task import Task


logger = logging.getLogger(__name__)


class TaskAsyncQueue:
    def __init__(self):
        self._queue: 'asyncio.Queue[Task | None]' = asyncio.Queue()
        self._closed = False

    async def put(self, task: Task | None):
        if self._closed:
            logger.error("Attempted to put a task into a closed queue.")
            raise RuntimeError("Queue is closed")
        if task is not None and not isinstance(task, Task):
            logger.error("Attempted to put an invalid task type into queue.")
            raise TypeError("Task must be of type Task")
        await self._queue.put(task)
        if task is not None:
            logger.debug(f"Task {task.id} put into async queue.")
        else:
            logger.debug("Shutdown signal (None) put into async queue.")

    async def get(self):
        item = await self._queue.get()
        if item is not None:
            logger.debug(f"Task {item.id} retrieved from async queue.")
        else:
            logger.debug("Shutdown signal (None) retrieved from async queue.")
        return item

    async def join(self) -> None:
        await self._queue.join()

    def task_done(self):
        self._queue.task_done()

    async def _get_raw(self) -> Task | None:
        return await self._queue.get()

    async def _signal_shutdown(self, num_workers: int) -> None:
        logger.info(f"Signaling shutdown to {num_workers} workers.")
        for _ in range(num_workers):
            await self._queue.put(None)
        self._closed = True