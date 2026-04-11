import pytest

from src.sources.task_sources import GeneratorSource

def test_add_param():
    source = GeneratorSource(seed=42, count=5)
    with pytest.raises(AttributeError):
        source.new_param = "new_param"

def test_source():
    source = GeneratorSource(seed=42, count=5)
    tasks = list(source.get_tasks())
    assert len(tasks) == 5