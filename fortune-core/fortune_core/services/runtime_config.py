from __future__ import annotations
from fortune_core.models.runtime_config import FortuneRuntimeConfig
class FortuneRuntimeConfigService:
    def __init__(
        self,
        config: FortuneRuntimeConfig | None = None,
    ) -> None:
        self._config = config or FortuneRuntimeConfig()
    def get(self) -> FortuneRuntimeConfig:
        return self._config
    def as_dict(self) -> dict[str, object]:
        return self._config.to_dict()