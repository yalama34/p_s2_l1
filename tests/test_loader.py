import pytest

from src.engine.task_loader import TaskLoader
from src.sources.task_sources import GeneratorSource


def test_add_valid_source(valid_source):
    loader: TaskLoader = TaskLoader()
    loader.add_source(valid_source)
    assert list(loader.get_tasks()) == []


def test_add_invalid_source(invalid_source):
    loader: TaskLoader = TaskLoader()
    with pytest.raises(TypeError):
        loader.add_source(invalid_source)


def test_change_tasks():
    loader: TaskLoader = TaskLoader()
    source: GeneratorSource = GeneratorSource(seed=42, count=5)
    loader.add_source(source)

    tasks = list(loader.get_tasks())
    tasks.append("break")

    assert len(list(loader.get_tasks())) == 5


def test_clear_tasks():
    """Повторные обходы независимы: внутренние источники не очищаются мутацией списка."""
    loader: TaskLoader = TaskLoader()
    source: GeneratorSource = GeneratorSource(seed=42, count=5)
    loader.add_source(source)
    assert len(list(loader.get_tasks())) == 5
    assert len(list(loader.get_tasks())) == 5
