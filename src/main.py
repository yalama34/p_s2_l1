"""Демо: загрузчик, несколько источников, очередь с повторным обходом."""

from __future__ import annotations

from pathlib import Path
from typing import Iterator

from src.engine.queue import TaskQueue
from src.engine.task import Task
from src.engine.task_loader import TaskLoader
from src.sources.task_sources import APISource, FileSource, GeneratorSource


def _example_file_path() -> Path:
    return Path(__file__).resolve().parents[1] / "example.txt"


def main() -> None:
    loader = TaskLoader()
    loader.add_source(FileSource(str(_example_file_path())))
    loader.add_source(APISource("https://api.example.com"))
    loader.add_source(GeneratorSource(seed=42, count=10))

    def task_factory() -> Iterator[Task]:
        yield from loader.get_tasks()

    queue = TaskQueue(task_source_factory=task_factory)

    first = list(queue)
    second = list(queue)
    print(f"First iteration: {len(first)} tasks")
    print(f"Second iteration: {len(second)} tasks")

    print("TaskQueue:")
    example = list(queue)
    for task in example:
        print(task)



if __name__ == "__main__":
    main()