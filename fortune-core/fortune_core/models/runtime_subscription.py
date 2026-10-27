from __future__ import annotations
from dataclasses import dataclass
@dataclass(frozen=True)
class FortuneRuntimeSubscription:
    subscription_id: str
    event_type: str
    active: bool = True
    def to_dict(self) -> dict[str, str | bool]:
        return {
            "subscription_id": self.subscription_id,
            "event_type": self.event_type,
            "active": self.active,
        }
