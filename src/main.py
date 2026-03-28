from pathlib import Path

from .task_engine.task_loader import TaskLoader
from .task_engine.task_sources import APISource, FileSource, GeneratorSource


def main() -> None:
    root = Path(__file__).resolve().parent.parent
    example_path = root / "example.txt"

    api_source = APISource(url="http://example.com")
    file_source = FileSource(path=str(example_path))
    generator_source = GeneratorSource(seed=13, count=5)
    loader = TaskLoader()

    loader.add_source(api_source)
    loader.add_source(file_source)
    loader.add_source(generator_source)

    tasks = loader.get_tasks()
    for task in tasks:
        print(task)


if __name__ == "__main__":
    main()