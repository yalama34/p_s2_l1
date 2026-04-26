import asyncio
import pytest

from src.engine.executor import AsyncTaskExecutor
from src.engine.task import Task
from src.contracts.handler import TaskHandler
from src.engine.executor_errors import ExecutorNotStartedError, HandlerRegistrationError
from src.engine.task_errors import TaskError


class DummyHandler:
    def __init__(self):
        self.handled_tasks = []
        self.raise_task_error = False
        self.raise_exception = False

    async def handle(self, task: Task):
        self.handled_tasks.append(task)
        if self.raise_task_error:
            raise TaskError("dummy task error")
        if self.raise_exception:
            raise ValueError("dummy exception")


def test_executor_init():
    executor = AsyncTaskExecutor(workers=5)
    assert executor._workers == 5
    assert not executor._running
    assert executor.errors == []


def test_executor_register_handler():
    executor = AsyncTaskExecutor()
    handler = DummyHandler()
    executor.register_handler(handler)
    assert executor._handler is handler

    with pytest.raises(TypeError, match="Task handler must be of type TaskHandler"):
        executor.register_handler("not a handler")


@pytest.mark.asyncio
async def test_executor_submit_not_started():
    executor = AsyncTaskExecutor()
    with pytest.raises(ExecutorNotStartedError, match="Executor is not running"):
        await executor.submit(Task("test", 1))


@pytest.mark.asyncio
async def test_executor_context_manager_and_execution():
    executor = AsyncTaskExecutor(workers=2)
    handler = DummyHandler()
    
    tasks = [Task("t1", 1), Task("t2", 2)]
    
    async with executor:
        executor.register_handler(handler)
        for t in tasks:
            await executor.submit(t)
            
        await executor.wait_all()
        
    assert len(handler.handled_tasks) == 2
    assert tasks[0] in handler.handled_tasks
    assert tasks[1] in handler.handled_tasks
    assert executor.errors == []


@pytest.mark.asyncio
async def test_executor_handler_task_error():
    executor = AsyncTaskExecutor(workers=1)
    handler = DummyHandler()
    handler.raise_task_error = True
    
    async with executor:
        executor.register_handler(handler)
        await executor.submit(Task("test", 1))
        await executor.wait_all()
        
    assert len(executor.errors) == 1
    assert isinstance(executor.errors[0], TaskError)


@pytest.mark.asyncio
async def test_executor_handler_exception():
    executor = AsyncTaskExecutor(workers=1)
    handler = DummyHandler()
    handler.raise_exception = True
    
    async with executor:
        executor.register_handler(handler)
        await executor.submit(Task("test", 1))
        await executor.wait_all()
        
    assert len(executor.errors) == 1
    assert isinstance(executor.errors[0], ValueError)
