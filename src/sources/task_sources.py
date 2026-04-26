from __future__ import annotations

import random
from typing import Any, Iterator

from src.engine.task import Task


class FileSource:
    __slots__ = ("_path",)

    def __init__(self, path: str) -> None:
        self._path: str = path

    def get_tasks(self) -> Iterator[Task]:
        try:
            with open(self._path, encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if not line:
                        continue
                    parts = line.split("|")
                    if len(parts) != 2:
                        raise ValueError("Invalid line '{}'".format(line))
                    description = parts[0].strip()
                    priority = int(parts[1].strip())
                    task = Task(
                        description=description,
                        priority=priority,
                    )
                    yield task

        except FileNotFoundError:
            raise FileNotFoundError(f"File '{self._path}' not found") from None


class GeneratorSource:
    __slots__ = ("_seed", "_count", "_descriptions", "_priorities")

    def __init__(self, seed: int, count: int) -> None:
        self._descriptions = ("desc1", "desc2", "desc3", "desc4", "desc5")
        self._priorities = (1, 2, 3, 4, 5)
        self._count = count
        self._seed = seed

    def get_tasks(self) -> Iterator[Task]:
        random.seed(self._seed)
        for _ in range(self._count):
            task = Task(
                description=random.choice(self._descriptions),
                priority=random.choice(self._priorities),
            )
            yield task


class APISource:
    __slots__ = ("_url", "_mock_api_data")

    def __init__(self, url: str) -> None:
        self._url: str = url
        self._mock_api_data: dict[str, dict[str, Any]] = {
            "Task_1": {
                "description": "desc1",
                "priority": 3,
            },
            "Task_2": {
                "description": "desc2",
                "priority": 1,
            },
        }

    def get_tasks(self) -> Iterator[Task]:
        for key, row in self._mock_api_data.items():
            task = Task(
                description=str(row["description"]),
                priority=int(row["priority"]),
            )
            yield task
