from __future__ import annotations
from fortune_core.models.runtime_capability import FortuneRuntimeCapability
class FortuneRuntimeCapabilityService:
    def __init__(self) -> None:
        self._items = (
            FortuneRuntimeCapability(
                name="fortune-home",
                enabled=True,
                description="Hubホーム情報",
                operations=("home",),
            ),
            FortuneRuntimeCapability(
                name="fortune-quick",
                enabled=True,
                description="質問からのクイック占い",
                operations=("quick",),
            ),
            FortuneRuntimeCapability(
                name="fortune-today",
                enabled=True,
                description="当日のフォーチュン情報",
                operations=("today",),
            ),
            FortuneRuntimeCapability(
                name="cache",
                enabled=True,
                description="Runtime結果キャッシュ",
                operations=("home", "quick", "today"),
            ),
            FortuneRuntimeCapability(
                name="event-log",
                enabled=True,
                description="Runtimeイベント記録",
                operations=("home", "quick", "today"),
            ),
            FortuneRuntimeCapability(
                name="audit",
                enabled=True,
                description="実行監査記録",
                operations=("home", "quick", "today"),
            ),
            FortuneRuntimeCapability(
                name="batch",
                enabled=True,
                description="複数Runtime要求の処理",
                operations=("batch",),
            ),
        )
    def list(self) -> list[FortuneRuntimeCapability]:
        return list(self._items)
    def get(self, name: str) -> FortuneRuntimeCapability | None:
        return next(
            (item for item in self._items if item.name == name),
            None,
        )