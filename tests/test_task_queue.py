import pytest

from src.engine.enums import TaskStatus
from src.engine.iterator import TaskIterator
from src.engine.queue import TaskQueue
from src.engine.task import Task


def get_tasks(*descriptions: str):
    for d in descriptions:
        yield Task(d, 1, TaskStatus.NEW)


def test_task_iterator_iter_returns_self_and_yields() -> None:
    it = TaskIterator(get_tasks("a", "b"))
    assert it.__iter__() is it
    assert next(it).description == "a"
    assert next(it).description == "b"
    with pytest.raises(StopIteration):
        next(it)


def test_task_queue_iter_yieldsget_tasks() -> None:
    def factory():
        yield from get_tasks("x", "y")

    q = TaskQueue(factory)
    assert [t.description for t in q] == ["x", "y"]


def test_task_queue_each_iteration_calls_factory() -> None:
    calls = 0

    def factory():
        nonlocal calls
        calls += 1
        yield Task("only", 2, TaskStatus.NEW)

    q = TaskQueue(factory)
    assert len(list(q)) == 1
    assert len(list(q)) == 1
    assert calls == 2


def test_task_queue_filter_yields_matching() -> None:
    def factory():
        yield Task("a", 1, TaskStatus.NEW)
        yield Task("b", 3, TaskStatus.NEW)
        yield Task("c", 5, TaskStatus.NEW)

    q = TaskQueue(factory)
    out = list(q.filter(lambda t: t.priority >= 3))
    assert [t.description for t in out] == ["b", "c"]


def test_task_queue_filter_requires_callable() -> None:
    q = TaskQueue(lambda: iter(()))
    with pytest.raises(TypeError, match="Mask must be callable"):
        list(q.filter("not callable"))
