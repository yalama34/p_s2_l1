import pytest

from src.engine.executor_errors import ExecutorNotStartedError, HandlerRegistrationError

def test_executor_not_started_error():
    err = ExecutorNotStartedError("test msg")
    assert str(err) == "test msg"
    assert err.message == "test msg"

def test_handler_registration_error():
    err = HandlerRegistrationError("test msg")
    assert str(err) == "test msg"
    assert err.message == "test msg"
