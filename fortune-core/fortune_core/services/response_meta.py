from __future__ import annotations
import hashlib
from datetime import datetime, timezone
from ..models.fortune_response_meta import FortuneResponseMeta
class FortuneResponseMetaService:
    API_VERSION = "1.0"
    SERVICE = "fortune-hub"
    def create(
        self,
        *,
        question: str,
        theme: str,
        system_count: int,
    ) -> FortuneResponseMeta:
        raw = (
            f"{question}|{theme}|"
            f"{datetime.now(timezone.utc).isoformat()}"
        )
        request_id = hashlib.sha256(
            raw.encode("utf-8")
        ).hexdigest()[:20]
        return FortuneResponseMeta(
            api_version=self.API_VERSION,
            service=self.SERVICE,
            request_id=f"req-{request_id}",
            theme=theme,
            system_count=system_count,
            generated_at=datetime.now(
                timezone.utc
            ).isoformat(),
        )
