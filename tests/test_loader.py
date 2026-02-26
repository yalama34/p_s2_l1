import pytest
from src.task_loader import TaskLoader
from src.task_sources import GeneratorSource

def test_add_valid_source(valid_source):
    loader: TaskLoader = TaskLoader()
    loader.add_source(valid_source)
    assert len(loader.get_tasks()) == 0

def test_add_invalid_source(invalid_source):
    loader: TaskLoader = TaskLoader()
    with pytest.raises(TypeError):
        loader.add_source(invalid_source)

def test_change_tasks():
    loader: TaskLoader = TaskLoader()
    source: GeneratorSource = GeneratorSource(seed=42, count=5)
    loader.add_source(source)

    tasks = loader.get_tasks()
    tasks.append("break")

    assert len(loader.get_tasks()) == 5

def test_clear_tasks():
    loader: TaskLoader = TaskLoader()
    source: GeneratorSource = GeneratorSource(seed=42, count=5)
    loader.add_source(source)
    loader.clear_tasks()
    assert len(loader.get_tasks()) == 0
