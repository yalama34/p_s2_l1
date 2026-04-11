import datetime
from datetime import timezone
from uuid import UUID

import pytest

from src.descriptors.descriptors import (
    CreatedAtDescriptor,
    IsReadyDescriptor,
    PriorityDescriptor,
    StatusDescriptor,
)
from src.engine.enums import TaskStatus
from src.engine.task import Task
from src.engine.task_errors import InvalidCreationDateError, InvalidPriorityError, InvalidStatusError


def test_invalid_priority():
    with pytest.raises(InvalidPriorityError):
        Task("d", 6)


def test_invalid_created_at():
    with pytest.raises(InvalidCreationDateError):
        Task("d", 5, TaskStatus.NEW, 11)  # type: ignore[arg-type]
    with pytest.raises(InvalidCreationDateError):
        Task("d", 5, TaskStatus.NEW, datetime.datetime.now() + datetime.timedelta(days=1))


def test_invalid_status():
    with pytest.raises(InvalidStatusError):
        Task("d", 5, "AAAAAAA")


def test_created_at_default():
    before = datetime.datetime.now()
    task = Task("d", 5)
    after = datetime.datetime.now()
    assert before <= task._created_at <= after
    assert isinstance(task.created_at, datetime.datetime)
    assert isinstance(task.id, UUID)


def test_private_fields_match_public_values():
    fixed = datetime.datetime(2020, 6, 15, 12, 30, 45)
    task = Task("d", 5, TaskStatus.IN_PROGRESS, fixed)
    assert task.id == task._id
    assert task.status == task._status
    assert task.description == task._description
    assert task.priority == task._priority
    assert task._created_at == fixed


def test_non_data_descriptor():
    task = Task("d", 5, TaskStatus.NEW)
    with pytest.raises(AttributeError):
        task.is_ready = False


def test_descriptors_on_class_return_descriptor() -> None:
    assert isinstance(Task.priority, PriorityDescriptor)
    assert isinstance(Task.created_at, CreatedAtDescriptor)
    assert isinstance(Task.status, StatusDescriptor)
    assert isinstance(Task.is_ready, IsReadyDescriptor)


def test_delete_descriptor_backed_attributes() -> None:
    task = Task("x", 3, TaskStatus.DONE)
    del task.priority
    del task.created_at
    del task.status
    assert task.priority is None
    assert task.created_at is None
    assert task.status is None


def test_created_at_timezone_aware_past_accepted() -> None:
    past = datetime.datetime(2000, 1, 1, 12, 0, 0, tzinfo=timezone.utc)
    task = Task("x", 1, TaskStatus.NEW, past)
    assert task.created_at == past


def test_is_ready_read_on_instance() -> None:
    task = Task("d", 5, TaskStatus.NEW)
    assert task.is_ready is False
