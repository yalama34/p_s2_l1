import pytest
from src.task_sources import FileSource

def test_add_param(temp_valid_file):
    source = FileSource(path=temp_valid_file)
    with pytest.raises(AttributeError):
        source.new_param = "new_param"

def test_invalid_file(temp_invalid_file):
    source = FileSource(path=temp_invalid_file)
    with pytest.raises(ValueError):
        source.get_tasks()

def test_invalid_line(temp_invalid_line_file):
    source = FileSource(path=temp_invalid_line_file)
    with pytest.raises(ValueError):
        source.get_tasks()

def test_invalid_file_path():
    source = FileSource(path="blablabla")
    with pytest.raises(FileNotFoundError):
        source.get_tasks()

def test_empty_line(temp_empty_line_file):
    source = FileSource(path=temp_empty_line_file)
    tasks = source.get_tasks()
    assert len(tasks) == 2


def test_source(temp_valid_file):
    source = FileSource(path=temp_valid_file)
    tasks = source.get_tasks()
    assert len(tasks) == 2 and isinstance(tasks, list)