from __future__ import annotations
from datetime import datetime, timezone
from typing import Any
def fortune_envelope(
    *,
    system: str,
    result: dict[str, Any],
) -> dict[str, Any]:
    return {
        "service": "fortune-project",
        "version": "3.0",
        "system": system,
        "created_at": datetime.now(
            timezone.utc
        ).isoformat(),
        "result": result,
    }