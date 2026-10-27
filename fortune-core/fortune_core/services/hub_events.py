from __future__ import annotations
import hashlib
import json
from collections import deque
from threading import RLock
from typing import Any
from fortune_core.models.hub_event import HubEvent
class FortuneHubEventService:
    def __init__(self, max_events: int = 500) -> None:
        self.max_events = max(1, max_events)
        self._events: deque[HubEvent] = deque(maxlen=self.max_events)
        self._lock = RLock()
    def emit(
        self,
        event_type: str,
        user_key: str,
        operation: str,
        theme: str,
        payload: dict[str, Any] | None = None,
    ) -> HubEvent:
        body = {
            "event_type": event_type,
            "user_key": user_key,
            "operation": operation,
            "theme": theme,
            "payload": payload or {},
            "index": len(self._events),
        }
        event_id = hashlib.sha256(
            json.dumps(body, ensure_ascii=False, sort_keys=True).encode("utf-8")
        ).hexdigest()[:20]
        event = HubEvent(
            event_id=event_id,
            event_type=event_type,
            user_key=user_key,
            operation=operation,
            theme=theme,
            payload=payload or {},
        )
        with self._lock:
            self._events.append(event)
        return event
    def list(
        self,
        user_key: str | None = None,
        event_type: str | None = None,
    ) -> list[HubEvent]:
        with self._lock:
            events = list(self._events)
        if user_key is not None:
            events = [event for event in events if event.user_key == user_key]
        if event_type is not None:
            events = [event for event in events if event.event_type == event_type]
        return events
    def count(self) -> int:
        with self._lock:
            return len(self._events)