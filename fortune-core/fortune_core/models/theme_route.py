from __future__ import annotations
from dataclasses import dataclass
@dataclass(frozen=True)
class FortuneThemeRoute:
    theme: str
    primary_system: str
    secondary_systems: tuple[str, ...]
    recommended_operation: str
    keywords: tuple[str, ...]
    def to_dict(self) -> dict[str, object]:
        return {
            "theme": self.theme,
            "primary_system": self.primary_system,
            "secondary_systems": list(self.secondary_systems),
            "recommended_operation": self.recommended_operation,
            "keywords": list(self.keywords),
        }
