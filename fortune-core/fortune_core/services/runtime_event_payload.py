from __future__ import annotations

from typing import Any

from fortune_core.models.hub_event import HubEvent


class FortuneRuntimeEventPayloadService:
    def build(
        self,
        event: HubEvent,
    ) -> dict[str, Any]:
        return {
            "event": {
                "id": event.event_id,
                "type": event.event_type,
                "timestamp": event.timestamp,
            },
            "user": {
                "key": event.user_key,
            },
            "runtime": {
                "operation": event.operation,
                "theme": event.theme,
            },
            "payload": event.payload,
        }