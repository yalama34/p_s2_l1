import pytest

from src.engine.enums import TaskStatus


@pytest.mark.parametrize(
    ("current", "expected"),
    [
        (TaskStatus.NEW, TaskStatus.IN_PROGRESS),
        (TaskStatus.IN_PROGRESS, TaskStatus.DONE),
        (TaskStatus.DONE, TaskStatus.NEW),
        (TaskStatus.CANCELLED, TaskStatus.NEW),
    ],
)
def test_get_next_status_sequence(current: TaskStatus, expected: TaskStatus) -> None:
    assert TaskStatus.get_next_status(current) is expected


def test_get_next_status_returns_member() -> None:
    for current in TaskStatus:
        nxt = TaskStatus.get_next_status(current)
        assert isinstance(nxt, TaskStatus)


def test_get_next_status_invalid_member_raises() -> None:
    class NotAStatus:
        pass

    with pytest.raises(ValueError):
        TaskStatus.get_next_status(NotAStatus())  # type: ignore[arg-type]
