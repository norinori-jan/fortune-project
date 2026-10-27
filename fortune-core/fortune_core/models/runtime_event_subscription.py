from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True)
class FortuneRuntimeEventSubscription:
    subscription_id: str
    user_key: str
    event_types: tuple[str, ...]
    enabled: bool = True
    metadata: dict[str, Any] = field(default_factory=dict)

    def accepts(self, event_type: str) -> bool:
        return (
            self.enabled
            and (
                not self.event_types
                or event_type in self.event_types
            )
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "subscription_id": self.subscription_id,
            "user_key": self.user_key,
            "event_types": list(self.event_types),
            "enabled": self.enabled,
            "metadata": self.metadata,
        }