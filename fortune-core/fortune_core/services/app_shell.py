from __future__ import annotations

from typing import Any

from fortune_core.services.runtime_ui_payload import (
    FortuneRuntimeUiPayloadService,
)
from fortune_core.services.ui_manifest import (
    FortuneUiManifestService,
)
from fortune_core.services.ui_shell import (
    FortuneUiShellService,
)


class FortuneAppShellService:
    def __init__(self) -> None:
        self.shell = FortuneUiShellService()
        self.payload = FortuneRuntimeUiPayloadService()
        self.manifest = FortuneUiManifestService()

    def build(
        self,
        user_key: str,
        theme: str = "general",
    ) -> dict[str, Any]:
        return {
            "app": {
                "name": "fortune-hub",
                "version": "1.0.0",
            },
            "manifest": self.manifest.build(),
            "shell": self.shell.build(
                user_key=user_key,
                theme=theme,
            ),
            "payload": self.payload.build(
                user_key=user_key,
                theme=theme,
            ).to_dict(),
        }