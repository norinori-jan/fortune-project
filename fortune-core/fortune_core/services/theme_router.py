from __future__ import annotations
from fortune_core.models.theme_route import FortuneThemeRoute
class FortuneThemeRouterService:
    def __init__(self) -> None:
        self._routes = {
            "general": FortuneThemeRoute(
                theme="general",
                primary_system="unified",
                secondary_systems=("tarot", "meihua"),
                recommended_operation="divine",
                keywords=("全体運", "流れ", "方向性"),
            ),
            "love": FortuneThemeRoute(
                theme="love",
                primary_system="tarot",
                secondary_systems=("unified", "meihua"),
                recommended_operation="draw",
                keywords=("恋愛", "関係", "出会い"),
            ),
            "work": FortuneThemeRoute(
                theme="work",
                primary_system="unified",
                secondary_systems=("five-elements", "tarot"),
                recommended_operation="divine",
                keywords=("仕事", "成長", "判断"),
            ),
            "money": FortuneThemeRoute(
                theme="money",
                primary_system="five-elements",
                secondary_systems=("unified", "tarot"),
                recommended_operation="analyze",
                keywords=("金運", "資産", "機会"),
            ),
            "health": FortuneThemeRoute(
                theme="health",
                primary_system="five-elements",
                secondary_systems=("unified", "meihua"),
                recommended_operation="analyze",
                keywords=("健康", "調整", "生活"),
            ),
        }
    def get(self, theme: str) -> FortuneThemeRoute:
        return self._routes.get(
            theme.lower(),
            self._routes["general"],
        )
    def list(self) -> list[FortuneThemeRoute]:
        return list(self._routes.values())
