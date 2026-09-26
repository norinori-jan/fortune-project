from __future__ import annotations
from datetime import date
import hashlib
from fortune_core.models.fortune_snapshot import FortuneSnapshot
class FortuneSnapshotService:
    @staticmethod
    def _make_id(
        question: str,
        system: str,
        theme: str,
        target_date: date,
    ) -> str:
        raw = (
            f"{question}|{system}|{theme}|"
            f"{target_date.isoformat()}"
        )
        return hashlib.sha256(
            raw.encode("utf-8")
        ).hexdigest()[:24]
    def create(
        self,
        question: str,
        system: str,
        theme: str,
        target_date: date,
        title: str,
        message: str,
        advice: str,
        keywords: tuple[str, ...] = (),
    ) -> FortuneSnapshot:
        return FortuneSnapshot(
            snapshot_id=self._make_id(
                question,
                system,
                theme,
                target_date,
            ),
            question=question,
            system=system,
            theme=theme,
            date_key=target_date.isoformat(),
            title=title,
            message=message,
            advice=advice,
            keywords=keywords,
        )

fortune-core/fortune_core/services/snapshot.py

from .fortune_snapshot import FortuneSnapshotService
__all__ = ["FortuneSnapshotService"]