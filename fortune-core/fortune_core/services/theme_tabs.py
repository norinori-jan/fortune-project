from __future__ import annotations

from fortune_core.models.theme_tab import FortuneThemeTab


class FortuneThemeTabService:
    TABS = (
        ("general", "総合", "全体の流れ"),
        ("love", "恋愛", "人間関係と恋愛"),
        ("work", "仕事", "仕事と挑戦"),
        ("money", "金運", "お金と計画"),
        ("health", "健康", "生活とコンディション"),
    )

    def build(
        self,
        active_theme: str = "general",
    ) -> list[FortuneThemeTab]:
        return [
            FortuneThemeTab(
                key=key,
                label=label,
                description=description,
                active=key == active_theme,
            )
            for key, label, description in self.TABS
        ]