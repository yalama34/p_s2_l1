from __future__ import annotations


import random
from datetime import datetime, timedelta
from typing import Any, Iterator

from src.engine.enums import TaskStatus
from src.engine.task import Task


def parse_status(raw: str) -> TaskStatus:
    """Map file/API strings (``in_progress``, ``in progress``, enum names) to :class:`TaskStatus`."""
    key = raw.strip().lower().replace(" ", "_")
    for member in TaskStatus:
        if member.name.lower() == key or member.value.lower().replace(" ", "_") == key:
            return member
    raise ValueError(f"Unknown task status: {raw!r}")


class FileSource:
    """Load tasks from a text file; each non-empty line is ``description|priority|status|created_at``."""
    __slots__ = ("_path",)

    def __init__(self, path: str) -> None:
        self._path: str = path

    def get_tasks(self) -> Iterator[Task]:
        """Read and parse the file; raise :exc:`FileNotFoundError` or :exc:`ValueError` on failure."""
        try:
            with open(self._path, encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if not line:
                        continue
                    parts = line.split("|")
                    if len(parts) != 4:
                        raise ValueError("Invalid line '{}'".format(line))
                    description = parts[0].strip()
                    priority = int(parts[1].strip())
                    status = parse_status(parts[2].strip())
                    created_raw = parts[3].strip()
                    created_at = datetime.strptime(created_raw, "%d.%m.%Y")
                    yield Task(
                        description=description,
                        priority=priority,
                        status=status,
                        created_at=created_at,
                    )

        except FileNotFoundError:
            raise FileNotFoundError(f"File '{self._path}' not found") from None


class GeneratorSource:
    """Produce ``count`` pseudo-random tasks using a fixed ``seed``."""
    __slots__ = ("_seed", "_count", "_descriptions", "_priorities", "_statuses", "_created_at_samples")

    def __init__(self, seed: int, count: int) -> None:
        self._descriptions = ("desc1", "desc2", "desc3", "desc4", "desc5")
        self._priorities = (1, 2, 3, 4, 5)
        self._statuses = tuple(TaskStatus)
        self._created_at_samples = (datetime.now(),)
        self._count = count
        self._seed = seed

    def get_tasks(self) -> Iterator[Task]:
        """Return ``count`` tasks with randomized fields (new UUID id each)."""
        random.seed(self._seed)
        for _ in range(self._count):
            created_raw = random.choice(self._created_at_samples)
            st = random.choice(self._statuses)
            yield Task(
                description=random.choice(self._descriptions),
                priority=random.choice(self._priorities),
                status=st,
                created_at=created_raw,
            )


class APISource:
    """Stub HTTP client: returns tasks from in-memory mock rows (ignores network)."""
    __slots__ = ("_url", "_mock_api_data")

    def __init__(self, url: str) -> None:
        self._url: str = url
        self._mock_api_data: dict[str, dict[str, Any]] = {
            "Task_1": {
                "description": "desc1",
                "priority": 3,
                "status": "new",
                "created_at": datetime.now(),
            },
            "Task_2": {
                "description": "desc2",
                "priority": 1,
                "status": "in_progress",
                "created_at": (datetime.now() - timedelta(hours=4)),
            },
        }

    def get_tasks(self) -> Iterator[Task]:
        """Build :class:`Task` instances from the built-in mock response body."""
        for row in self._mock_api_data.values():
            created_raw = row.get("created_at")
            created_at = created_raw if created_raw is not None else None
            yield Task(
                description=str(row["description"]),
                priority=int(row["priority"]),
                status=parse_status(str(row["status"])),
                created_at=created_at,
            )
