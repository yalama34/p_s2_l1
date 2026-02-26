from dataclasses import dataclass
from typing import Dict, Any

@dataclass(slots=True)
class Task:
    id: int
    payload: Dict[str, Any]