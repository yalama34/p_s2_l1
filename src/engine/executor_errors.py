class ExecutorError(Exception):
    pass

class ExecutorNotStartedError(ExecutorError):
    def __init__(self, message: str) -> None:
        self.message = message
        super().__init__(self.message)

class HandlerRegistrationError(ExecutorError):
    def __init__(self, message: str) -> None:
        self.message = message
        super().__init__(self.message)