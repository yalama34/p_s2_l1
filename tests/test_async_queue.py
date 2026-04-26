import asyncio
import pytest

from src.engine.async_queue import TaskAsyncQueue
from src.engine.task import Task


@pytest.mark.asyncio
async def test_task_async_queue_put_get():
    queue = TaskAsyncQueue()
    task = Task("test", 1)
    
    await queue.put(task)
    retrieved = await queue.get()
    
    assert retrieved is task


@pytest.mark.asyncio
async def test_task_async_queue_put_none():
    queue = TaskAsyncQueue()
    await queue.put(None)
    retrieved = await queue.get()
    assert retrieved is None


@pytest.mark.asyncio
async def test_task_async_queue_put_closed():
    queue = TaskAsyncQueue()
    queue._closed = True
    with pytest.raises(RuntimeError, match="Queue is closed"):
        await queue.put(Task("test", 1))


@pytest.mark.asyncio
async def test_task_async_queue_put_invalid_type():
    queue = TaskAsyncQueue()
    with pytest.raises(TypeError, match="Task must be of type Task"):
        await queue.put("not a task")


@pytest.mark.asyncio
async def test_task_async_queue_task_done_and_join():
    queue = TaskAsyncQueue()
    task = Task("test", 1)
    await queue.put(task)
    
    _ = await queue.get()
    queue.task_done()

    await asyncio.wait_for(queue.join(), timeout=0.1)


@pytest.mark.asyncio
async def test_task_async_queue_get_raw():
    queue = TaskAsyncQueue()
    task = Task("test", 1)
    await queue.put(task)
    retrieved = await queue._get_raw()
    assert retrieved is task


@pytest.mark.asyncio
async def test_task_async_queue_signal_shutdown():
    queue = TaskAsyncQueue()
    await queue._signal_shutdown(2)
    assert queue._closed is True
    assert await queue.get() is None
    assert await queue.get() is None
