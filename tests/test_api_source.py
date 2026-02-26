import pytest
from src.task_sources import APISource

def test_add_param(temp_valid_file):
    source = APISource(url="http://example.com")
    with pytest.raises(AttributeError):
        source.new_param = "new_param"

def test_source():
    source = APISource(url="http://example.com")
    tasks = source.get_tasks()
    assert len(tasks) == 2 and isinstance(tasks, list)