from typing import List, Dict, Any
from .task import Task
import json
from datetime import datetime
import datetime as dt
import random

class FileSource:
    """
    Source that get tasks from a file
    """
    __slots__ = ('_path',)

    def __init__(self, path: str):
        self._path: str = path

    def get_tasks(self) -> List[Task]:
        """
        Get all tasks from a file
        :return: list of tasks
        """
        output: List[Task] = []
        try:
            with open(self._path) as f:
                for line in f:
                    line: str = line.strip()
                    if not line:
                        continue
                    parts: List[str] = line.split('.', 1)
                    if len(parts) != 2:
                        raise ValueError("Invalid line '{}'".format(line))
                    task_id: int = int(parts[0].strip())
                    payload_str: str = parts[1].strip()
                    payload_dict: Dict[str, Any] = json.loads(payload_str)

                    task: Task = Task(id=task_id, payload=payload_dict)
                    output.append(task)
        except FileNotFoundError:
            raise FileNotFoundError(f"File '{self._path}' not found")
        except json.decoder.JSONDecodeError:
            raise ValueError(f"File '{self._path}' is not a valid json")
        return output

class GeneratorSource:
    """
    Source that generate tasks
    """
    __slots__ = ('_seed', '_payload_params', '_count',)
    def __init__(self, seed: int, count: int):
        self._payload_params: Dict[str, Any] = {
            "description": ["desc1", "desc2", "desc3", "desc4", "desc5"],
            "priority": ["1", "2", "3", "4", "5"],
            "status": ["new", "in_progress", "completed"],
            "created_at": [datetime.now().isoformat()],
            "is_expired": [False, True],
        }
        self._count: int = count
        self._seed: int = seed

    def get_tasks(self) -> List[Task]:
        random.seed(self._seed)
        output: List[Task] = []

        for task_id in range(self._count):
            payload: Dict[str, Any] = {}
            for payload_key, payload_values in self._payload_params.items():
                payload_value: Any = random.choice(payload_values)
                payload[payload_key]: str = payload_value
            task: Task = Task(id=task_id, payload=payload)
            output.append(task)
        return output

class APISource:
    __slots__ = ('_url', '_mock_api_data',)

    def __init__(self, url: str):
        self._url: str = url
        self._mock_api_data: Dict[str | Any] = {
            "Task_1": {
                "id": 1,
                "payload":{
                    "description": "desc1",
                    "priority": 3,
                    "status": "new",
                    "created_at": datetime.now().isoformat(),
                    "is_expired": False,
                }
            },
            "Task_2": {
                "id": 2,
                "payload":{
                    "description": "desc2",
                    "priority": 1,
                    "status": "in_progress",
                    "created_at": (datetime.now() - dt.timedelta(hours=4)).isoformat(),
                }
            }
        }

    def get_tasks(self) -> List[Task]:
        output: List[Task] = []
        for task in self._mock_api_data.values():
            output.append(Task(id=task["id"], payload=task["payload"]))
        return output
