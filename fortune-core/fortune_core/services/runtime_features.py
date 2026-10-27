from __future__ import annotations

from threading import RLock

from fortune_core.models.runtime_feature import FortuneRuntimeFeature


class FortuneRuntimeFeatureService:
    DEFAULTS = {
        "fortune_home": True,
        "fortune_quick": True,
        "fortune_today": True,
        "tarot": True,
        "meihua": True,
        "five_elements": True,
        "history": True,
        "favorites": True,
        "notifications": True,
        "sharing": True,
        "comparison": True,
    }

    def __init__(
        self,
        features: dict[str, bool] | None = None,
    ) -> None:
        self._features = dict(self.DEFAULTS)
        self._features.update(features or {})
        self._lock = RLock()

    def enabled(self, name: str) -> bool:
        with self._lock:
            return bool(self._features.get(name, False))

    def set(self, name: str, enabled: bool) -> FortuneRuntimeFeature:
        with self._lock:
            self._features[name] = enabled

        return FortuneRuntimeFeature(
            name=name,
            enabled=enabled,
        )

    def list(self) -> list[FortuneRuntimeFeature]:
        with self._lock:
            return [
                FortuneRuntimeFeature(
                    name=name,
                    enabled=enabled,
                )
                for name, enabled in sorted(
                    self._features.items()
                )
            ]