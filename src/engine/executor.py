import asyncio
import logging

from .async_queue import TaskAsyncQueue
from .task import Task
from ..contracts.handler import TaskHandler
from .executor_errors import ExecutorNotStartedError, HandlerRegistrationError
from .task_errors import TaskError


logger = logging.getLogger(__name__)


class AsyncTaskExecutor:
    def __init__(self, workers: int = 2) -> None:
        self._workers = workers
        self._queue: TaskAsyncQueue = TaskAsyncQueue()
        self._handler: TaskHandler | None = None
        self._worker_tasks: list[asyncio.Task[None]] = []
        self._errors: list[Exception] = []
        self._running = False

    def register_handler(self, handler: TaskHandler) -> None:
        if not isinstance(handler, TaskHandler):
            raise TypeError("Task handler must be of type TaskHandler")
        self._handler = handler

    async def submit(self, task: Task) -> None:
        if not self._running or self._queue is None:
            logger.error("Attempted to submit task to non-running executor.")
            raise ExecutorNotStartedError("Executor is not running. Use `async with` instead")
        logger.debug(f"Submitting task {task.id} to executor queue.")
        await self._queue.put(task)

    async def wait_all(self):
        if self._queue:
            await self._queue.join()

    @property
    def errors(self) -> list[Exception]:
        return self._errors

    async def __aenter__(self) -> 'AsyncTaskExecutor':
        logger.info(f"Starting executor with {self._workers} workers.")
        self._running = True
        self._queue = TaskAsyncQueue()
        self._worker_tasks = [
            asyncio.create_task(self._worker_loop(f"worker #{i}"))
            for i in range(self._workers)
        ]
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> bool:
        logger.info("Stopping executor. Waiting for workers to finish remaining tasks.")
        for _ in self._worker_tasks:
            await self._queue.put(None)
        await asyncio.gather(*self._worker_tasks, return_exceptions=True)
        self._running = False
        logger.info("Executor stopped.")
        return False

    async def _worker_loop(self, name: str) -> None:
        logger.info(f"{name}: Started.")
        while True:
            task = await self._queue.get()
            if task is None:
                logger.info(f"{name}: Received shutdown signal. Stopping.")
                self._queue.task_done()
                break
            try:
                if self._handler is None:
                    logger.error(f"{name}: Handler is not defined.")
                    raise HandlerRegistrationError("Handler is not defined. Use register_handler()")

                logger.debug(f"{name}: Starting task {task.id}")
                await self._handler.handle(task)
                logger.debug(f"{name}: Successfully completed task {task.id}")
            except HandlerRegistrationError as error:
                logger.error(f"{name}: {error}")
                self._errors.append(error)
                break  # Stop this worker if handler is missing
            except TaskError as error:
                logger.warning(f"{name}: Error executing task {task.id}: {error}")
                self._errors.append(error)
            except Exception as error:
                logger.error(f"{name}: Unexpected error executing task {task.id}: {error!r}")
                self._errors.append(error)
            finally:
                self._queue.task_done()