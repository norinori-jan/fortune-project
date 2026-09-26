from __future__ import annotations
from dataclasses import dataclass
@dataclass(frozen=True)
class FortuneRuntimeCapability:
    name: str
    enabled: bool
    description: str
    operations: tuple[str, ...]
    def to_dict(self) -> dict[str, object]:
        return {
            "name": self.name,
            "enabled": self.enabled,
            "description": self.description,
            "operations": list(self.operations),
        }
