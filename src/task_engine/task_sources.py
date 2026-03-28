from __future__ import annotations

"""Task source implementations: file, random generator, and API stub."""

import random
from datetime import datetime, timedelta
from typing import Any

from .task import Task

class FileSource:
    """Load tasks from a text file; each non-empty line is ``id|description|priority|status|created_at``."""
    __slots__ = ("_path",)

    def __init__(self, path: str) -> None:
        self._path: str = path

    def get_tasks(self) -> list[Task]:
        """Read and parse the file; raise :exc:`FileNotFoundError` or :exc:`ValueError` on failure."""
        output: list[Task] = []
        try:
            with open(self._path, encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if not line:
                        continue
                    parts = line.split("|")
                    if len(parts) != 5:
                        raise ValueError("Invalid line '{}'".format(line))
                    task_id = int(parts[0].strip())
                    description = parts[1].strip()
                    priority = int(parts[2].strip())
                    status = parts[3].strip()
                    created_raw = parts[4].strip()
                    created_at = datetime.strptime(created_raw, "%d.%m.%Y")
                    output.append(
                        Task(
                            id=task_id,
                            description=description,
                            priority=priority,
                            status=status,
                            created_at=created_at,
                        )
                    )
        except FileNotFoundError:
            raise FileNotFoundError(f"File '{self._path}' not found") from None
        return output


class GeneratorSource:
    """Produce ``count`` pseudo-random tasks using a fixed ``seed``."""
    __slots__ = ("_seed", "_count", "_descriptions", "_priorities", "_statuses", "_created_at_samples")

    def __init__(self, seed: int, count: int) -> None:
        self._descriptions = ("desc1", "desc2", "desc3", "desc4", "desc5")
        self._priorities = (1, 2, 3, 4, 5)
        self._statuses = ("new", "in_progress", "done", "cancelled")
        self._created_at_samples = (datetime.now(),)
        self._count = count
        self._seed = seed

    def get_tasks(self) -> list[Task]:
        """Return tasks with ids ``0 .. count-1`` and randomized fields."""
        random.seed(self._seed)
        output: list[Task] = []
        for task_id in range(self._count):
            created_raw = random.choice(self._created_at_samples)
            output.append(
                Task(
                    id=task_id,
                    description=random.choice(self._descriptions),
                    priority=random.choice(self._priorities),
                    status=random.choice(self._statuses),
                    created_at=created_raw,
                )
            )
        return output


class APISource:
    """Stub HTTP client: returns tasks from in-memory mock rows (ignores network)."""
    __slots__ = ("_url", "_mock_api_data")

    def __init__(self, url: str) -> None:
        self._url: str = url
        self._mock_api_data: dict[str, dict[str, Any]] = {
            "Task_1": {
                "id": 1,
                "description": "desc1",
                "priority": 3,
                "status": "new",
                "created_at": datetime.now(),
            },
            "Task_2": {
                "id": 2,
                "description": "desc2",
                "priority": 1,
                "status": "in_progress",
                "created_at": (datetime.now() - timedelta(hours=4)),
            },
        }

    def get_tasks(self) -> list[Task]:
        """Build :class:`Task` instances from the built-in mock response body."""
        output: list[Task] = []
        for row in self._mock_api_data.values():
            created_raw = row.get("created_at")
            created_at = created_raw if created_raw is not None else None
            output.append(
                Task(
                    id=int(row["id"]),
                    description=str(row["description"]),
                    priority=int(row["priority"]),
                    status=str(row["status"]),
                    created_at=created_at,
                )
            )
        return output
