from __future__ import annotations
import base64
import hashlib
import json
from fortune_core.models.fortune_share import FortuneShare
class FortuneShareService:
    def create(
        self,
        *,
        title: str,
        message: str,
        advice: str,
        system: str,
        theme: str,
        date_key: str,
    ) -> FortuneShare:
        payload = {
            "title": title,
            "message": message,
            "advice": advice,
            "system": system,
            "theme": theme,
            "date": date_key,
        }
        encoded = json.dumps(
            payload,
            ensure_ascii=False,
            sort_keys=True,
            separators=(",", ":"),
        )
        share_id = hashlib.sha256(
            encoded.encode("utf-8")
        ).hexdigest()[:16]
        return FortuneShare(
            share_id=share_id,
            title=title,
            message=message,
            advice=advice,
            system=system,
            theme=theme,
            date_key=date_key,
        )
    def encode(self, share: FortuneShare) -> str:
        raw = json.dumps(
            share.to_dict(),
            ensure_ascii=False,
            separators=(",", ":"),
        ).encode("utf-8")
        return base64.urlsafe_b64encode(raw).decode("ascii")
    def decode(self, value: str) -> dict:
        raw = base64.urlsafe_b64decode(
            value.encode("ascii")
        )
        return json.loads(
            raw.decode("utf-8")
        )
