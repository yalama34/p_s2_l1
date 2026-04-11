import enum
from typing import Optional


class TaskStatus(enum.Enum):
    NEW = "new"
    IN_PROGRESS = "in progress"
    DONE = "done"
    CANCELLED = "cancelled"

    @classmethod
    def get_next_status(cls, current: 'TaskStatus') -> Optional['TaskStatus']:
        statuses = list(cls)
        cur_index = statuses.index(current)
        print(cur_index)

        match cur_index:
            case 2 | 3:
                return statuses[0]
            case _:
                return statuses[cur_index + 1]