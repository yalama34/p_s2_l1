import uuid

from src.engine.task_errors import (
    InvalidCreationDateError,
    InvalidPriorityError,
    InvalidStatusError,
    StatusTransitionError,
    TaskAlreadyExistsError,
    TaskError,
    TaskNotFoundError,
)


def test_task_error_is_base() -> None:
    assert issubclass(TaskNotFoundError, TaskError)


def test_task_not_found_error() -> None:
    tid = uuid.uuid4()
    err = TaskNotFoundError(tid)
    assert err.task_id is tid
    assert str(err) == f"Task {tid} not found"


def test_task_already_exists_error() -> None:
    tid = uuid.uuid4()
    err = TaskAlreadyExistsError(tid)
    assert err.task_id is tid
    assert str(err) == f"Task {tid} already exists"


def test_invalid_priority_error() -> None:
    err = InvalidPriorityError(99)
    assert err.priority == 99
    assert "99" in str(err)


def test_status_transition_error() -> None:
    tid = uuid.uuid4()
    err = StatusTransitionError(tid, "done")
    assert err.task_id is tid
    assert err.status == "done"
    assert "done" in str(err) and str(tid) in str(err)


def test_invalid_creation_date_error() -> None:
    err = InvalidCreationDateError("ddddd")
    assert err.date == "ddddd"
    assert str(err) == "Excepted datetime format, got <class 'str'>"


def test_invalid_status_error() -> None:
    err = InvalidStatusError("fsdlkfjsdjkfjksdf")
    assert err.status == "fsdlkfjsdjkfjksdf"
    assert "fsdlkfjsdjkfjksdf" in str(err)
