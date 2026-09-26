from __future__ import annotations
from fortune_core.models.runtime_error import FortuneRuntimeError
class FortuneRuntimeException(Exception):
    def __init__(
        self,
        code: str,
        message: str,
        operation: str = "",
        request_id: str | None = None,
        details: dict | None = None,
    ) -> None:
        super().__init__(message)
        self.code = code
        self.message = message
        self.operation = operation
        self.request_id = request_id
        self.details = details or {}
    def to_model(self) -> FortuneRuntimeError:
        return FortuneRuntimeError(
            code=self.code,
            message=self.message,
            operation=self.operation,
            request_id=self.request_id,
            details=self.details,
        )
class UnsupportedOperationError(FortuneRuntimeException):
    def __init__(self, operation: str) -> None:
        super().__init__(
            code="UNSUPPORTED_OPERATION",
            message=f"Unsupported operation: {operation}",
            operation=operation,
        )
class InvalidThemeError(FortuneRuntimeException):
    def __init__(self, theme: str) -> None:
        super().__init__(
            code="INVALID_THEME",
            message=f"Invalid theme: {theme}",
            details={"theme": theme},
        )
class EmptyQuestionError(FortuneRuntimeException):
    def __init__(self) -> None:
        super().__init__(
            code="EMPTY_QUESTION",
            message="Question is required for this operation.",
        )