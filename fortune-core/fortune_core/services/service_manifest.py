from __future__ import annotations
from fortune_core.models.service_manifest import FortuneServiceManifest
class FortuneServiceManifestService:
    def __init__(self) -> None:
        self._manifests = (
            FortuneServiceManifest(
                name="unified",
                version="1.0",
                category="fortune",
                operations=("divine",),
                themes=("general", "love", "work", "money", "health"),
                description="統合型フォーチュン",
            ),
            FortuneServiceManifest(
                name="tarot",
                version="1.0",
                category="fortune",
                operations=("draw",),
                themes=("general", "love", "work", "money", "health"),
                description="タロット",
            ),
            FortuneServiceManifest(
                name="meihua",
                version="1.0",
                category="fortune",
                operations=("divine",),
                themes=("general", "love", "work", "money", "health"),
                description="梅花易数",
            ),
            FortuneServiceManifest(
                name="five-elements",
                version="1.0",
                category="analysis",
                operations=("analyze",),
                themes=("general", "love", "work", "money", "health"),
                description="五行分析",
            ),
            FortuneServiceManifest(
                name="shichu",
                version="1.0",
                category="profile",
                operations=("analyze",),
                themes=("general",),
                description="四柱プロフィール",
            ),
            FortuneServiceManifest(
                name="hub",
                version="1.0",
                category="orchestration",
                operations=("home", "quick", "today"),
                themes=("general", "love", "work", "money", "health"),
                description="Fortune Hub",
            ),
        )
    def list(self) -> list[FortuneServiceManifest]:
        return list(self._manifests)
    def get(self, name: str) -> FortuneServiceManifest | None:
        for manifest in self._manifests:
            if manifest.name == name:
                return manifest
        return None
    def names(self) -> tuple[str, ...]:
        return tuple(item.name for item in self._manifests)