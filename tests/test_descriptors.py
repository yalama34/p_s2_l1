import pytest

import datetime

from src.descriptors.descriptors import PriorityDescriptor, StatusDescriptor, CreatedAtDescriptor, IsReadyDescriptor
from src.task_engine.task_errors import InvalidPriorityError, InvalidCreationDateError, InvalidStatusError
from src.task_engine.task import Task

def test_invalid_priority():
    with pytest.raises(InvalidPriorityError):
        Task(1, "d", 6)

def test_invalid_created_at():
    with pytest.raises(InvalidCreationDateError):
        Task(1, "d", 5, "new", 11)
    with pytest.raises(InvalidCreationDateError):
        Task(1, "d", 5, "new", datetime.datetime.now() + datetime.timedelta(days=1))

def test_invalid_status():
    with pytest.raises(InvalidStatusError):
        Task(1, "d", 5, "AAAAAAA")

def test_invalid_id():
    with pytest.raises(ValueError):
        Task(-5, "d", 5)

def test_created_at_default():
    """Internal slot is datetime; public ``created_at`` is a formatted string from the descriptor."""
    before = datetime.datetime.now()
    task = Task(1, "d", 5)
    after = datetime.datetime.now()
    assert before <= task._created_at <= after
    assert task.created_at == task._created_at.strftime("%d.%m.%Y %H:%M:%S")


def test_private_fields_match_public_values():
    fixed = datetime.datetime(2020, 6, 15, 12, 30, 45)
    task = Task(1, "d", 5, "in_progress", fixed)
    assert task.id == task._id
    assert task.status == task._status
    assert task.description == task._description
    assert task.priority == task._priority
    assert task._created_at == fixed
    assert task.created_at == fixed.strftime("%d.%m.%Y %H:%M:%S")

def test_non_data_descriptor():
    task = Task(1, "d", 5, "new")
    assert task.is_ready
    with pytest.raises(AttributeError):
        task.is_ready = False