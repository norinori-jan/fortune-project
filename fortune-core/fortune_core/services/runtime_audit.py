from __future__ import annotations
import hashlib
import json
from collections import deque
from threading import RLock
from typing import Any
from fortune_core.models.runtime_audit import FortuneRuntimeAudit
class FortuneRuntimeAuditService:
    def __init__(self, max_items: int = 1000) -> None:
        self.max_items = max(1, max_items)
        self._items: deque[FortuneRuntimeAudit] = deque(
            maxlen=self.max_items
        )
        self._lock = RLock()
    def record(
        self,
        request_id: str,
        event_type: str,
        operation: str,
        user_key: str,
        success: bool,
        details: dict[str, Any] | None = None,
    ) -> FortuneRuntimeAudit:
        payload = {
            "request_id": request_id,
            "event_type": event_type,
            "operation": operation,
            "user_key": user_key,
            "success": success,
            "details": details or {},
        }
        audit_id = hashlib.sha256(
            json.dumps(
                payload,
                ensure_ascii=False,
                sort_keys=True,
            ).encode("utf-8")
        ).hexdigest()[:24]
        item = FortuneRuntimeAudit(
            audit_id=audit_id,
            request_id=request_id,
            event_type=event_type,
            operation=operation,
            user_key=user_key,
            success=success,
            details=details or {},
        )
        with self._lock:
            self._items.append(item)
        return item
    def list(
        self,
        user_key: str | None = None,
        request_id: str | None = None,
    ) -> list[FortuneRuntimeAudit]:
        with self._lock:
            items = list(self._items)
        if user_key is not None:
            items = [
                item for item in items
                if item.user_key == user_key
            ]
        if request_id is not None:
            items = [
                item for item in items
                if item.request_id == request_id
            ]
        return items