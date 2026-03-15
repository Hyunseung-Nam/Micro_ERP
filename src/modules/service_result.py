from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class ServiceResult:
    """Service layer standard response."""

    ok: bool
    message: str = ""
    payload: Any = None


SUCCESS_EMPTY = ServiceResult(ok=True, message="")
