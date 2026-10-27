from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class FortuneRuntimeDelivery:
    delivery_id: str
    subscription_id: str
    event_type: str
    status: str
    payload: dict[str, Any]
    error: str | None = None

    def to_dict(self) -> dict[str, Any]:
        return {
            "delivery_id": self.delivery_id,
            "subscription_id": self.subscription_id,
            "event_type": self.event_type,
            "status": self.status,
            "payload": self.payload,
            "error": self.error,
        }