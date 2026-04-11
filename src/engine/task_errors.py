class TaskError(Exception):
    """Base class for task subsystem errors."""
    pass


class TaskNotFoundError(TaskError):
    """Raised when a task id does not exist in a collection."""

    def __init__(self, task_id):
        self.task_id = task_id
        super().__init__(f"Task {self.task_id} not found")


class TaskAlreadyExistsError(TaskError):
    """Raised when inserting a task whose id is already present."""

    def __init__(self, task_id):
        self.task_id = task_id
        super().__init__(f"Task {self.task_id} already exists")


class InvalidPriorityError(TaskError):
    """Raised when priority is not an integer in the allowed range."""

    def __init__(self, priority):
        self.priority = priority
        super().__init__(f"Priority '{self.priority}' is invalid")


class StatusTransitionError(TaskError):
    """Raises when status transition fails."""

    def __init__(self, task_id, status):
        self.task_id = task_id
        self.status = status
        super().__init__(f"Failed switch status '{self.status}' for task '{self.task_id}'")


class InvalidCreationDateError(TaskError):
    """Raised when ``created_at`` is not a datetime or is in the future."""

    def __init__(self, date):
        self.date = date
        super().__init__(f"Excepted datetime format, got {type(date)}")


class InvalidStatusError(TaskError):
    """Raised when status is not one of the allowed string values."""

    def __init__(self, status):
        self.status = status
        super().__init__(f"Status '{self.status}' is invalid")
