import pytest
import pathlib

@pytest.fixture
def temp_valid_file(tmp_path: pathlib.Path) -> str:
    file_path = tmp_path / "test.txt"
    data = [
        "1. {\"test\": \"test1\"}",
        "2. {\"test\": \"test2\"}",
    ]
    file_path.write_text("\n".join(data))
    return str(file_path)

@pytest.fixture
def temp_invalid_file(tmp_path: pathlib.Path) -> str:
    file_path = tmp_path / "test.txt"
    data = [
        "1. blablabla",
        "2. gonna break",
    ]
    file_path.write_text("\n".join(data))
    return str(file_path)

@pytest.fixture
def temp_invalid_line_file(tmp_path: pathlib.Path) -> str:
    file_path = tmp_path / "test.txt"
    data = [
        "1. {\"test\": \"test1\"}",
        "2 {\"test\": \"test2\"}",
    ]
    file_path.write_text("\n".join(data))
    return str(file_path)

@pytest.fixture
def temp_empty_line_file(tmp_path: pathlib.Path) -> str:
    file_path = tmp_path / "test.txt"
    data = [
        "1. {\"test\": \"test1\"}",
        "  ",
        "         ",
        "2. {\"test\": \"test2\"}",
    ]
    file_path.write_text("\n".join(data))
    return str(file_path)

@pytest.fixture
def valid_source():
    class MockValidSource:
        def get_tasks(self):
            return []
    return MockValidSource()

@pytest.fixture
def invalid_source():
    class MockInvalidSource:
        def hello_world(self):
            return "hello world"
    return MockInvalidSource()
