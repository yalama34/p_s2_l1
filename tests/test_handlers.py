import asyncio
import pytest
from unittest.mock import patch

from src.engine.task import Task
from src.engine.enums import TaskStatus
from src.engine.task_errors import TaskError
from src.handlers.priority_handler import PriorityHandler
from src.handlers.random_handler import RandomHandler


@pytest.mark.asyncio
async def test_priority_handler():
    handler = PriorityHandler()
    task = Task("test", 2)
    assert task.status == TaskStatus.NEW

    with patch("asyncio.sleep", new_callable=pytest.MonkeyPatch) as mock_sleep:
        async def dummy_sleep(delay):
            assert delay == 0.2
            
        with patch('asyncio.sleep', side_effect=dummy_sleep):
            await handler.handle(task)
            
    assert task.status == TaskStatus.DONE


@pytest.mark.asyncio
async def test_random_handler_success():
    handler = RandomHandler(seed=42)
    task = Task("test", 1)
    
    with patch("random.random", return_value=0.5):
        await handler.handle(task)
        
    assert task.status == TaskStatus.DONE


@pytest.mark.asyncio
async def test_random_handler_failure():
    handler = RandomHandler(seed=42)
    task = Task("test", 1)
    
    with patch("random.random", return_value=0.1):
        with pytest.raises(TaskError, match="Task .* failed"):
            await handler.handle(task)
            
    assert task.status == TaskStatus.CANCELLED
