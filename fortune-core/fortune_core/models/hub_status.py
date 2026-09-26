from __future__ import annotations
from dataclasses import dataclass
from typing import Any
@dataclass(frozen=True)
class HubStatus:
    service: str
    version: str
    status: str
    providers: tuple[str, ...]
    operations: tuple[str, ...]
    features: tuple[str, ...]
    metadata: dict[str, Any]
    def to_dict(self) -> dict[str, Any]:
        return {
            "service": self.service,
            "version": self.version,
            "status": self.status,
            "providers": list(self.providers),
            "operations": list(self.operations),
            "features": list(self.features),
            "metadata": self.metadata,
        }
