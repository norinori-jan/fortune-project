from __future__ import annotations
from typing import Any
from fortune_core.models.api_meta import FortuneApiMeta
def fortune_response(
    result: Any,
    *,
    service: str = "fortune-platform",
    version: str = "2",
) -> dict[str, Any]:
    if hasattr(result, "to_dict"):
        payload = result.to_dict()
    else:
        payload = result
    return {
        "meta": FortuneApiMeta(
            service=service,
            version=version,
            deterministic=True,
        ).to_dict(),
        "result": payload,
    }
