from __future__ import annotations

from fortune_core.models.runtime_discovery import (
    FortuneRuntimeDiscoveryItem,
)


class FortuneRuntimeDiscoveryService:
    ITEMS = (
        FortuneRuntimeDiscoveryItem(
            key="daily",
            title="今日の運勢",
            description="今日の流れと行動のヒントを確認します。",
            category="daily",
            operation="today",
            theme="general",
            keywords=("今日", "運勢", "日運"),
        ),
        FortuneRuntimeDiscoveryItem(
            key="love",
            title="恋愛運",
            description="恋愛テーマを中心に占います。",
            category="theme",
            operation="quick",
            theme="love",
            keywords=("恋愛", "出会い", "関係"),
        ),
        FortuneRuntimeDiscoveryItem(
            key="work",
            title="仕事運",
            description="仕事や挑戦の方向性を確認します。",
            category="theme",
            operation="quick",
            theme="work",
            keywords=("仕事", "キャリア", "挑戦"),
        ),
        FortuneRuntimeDiscoveryItem(
            key="money",
            title="金運",
            description="お金に関するテーマを整理します。",
            category="theme",
            operation="quick",
            theme="money",
            keywords=("お金", "金運", "収支"),
        ),
        FortuneRuntimeDiscoveryItem(
            key="health",
            title="健康運",
            description="生活リズムや整え方のヒントを確認します。",
            category="theme",
            operation="quick",
            theme="health",
            keywords=("健康", "生活", "休息"),
        ),
        FortuneRuntimeDiscoveryItem(
            key="general",
            title="総合運",
            description="複数の占術を横断して全体を確認します。",
            category="system",
            operation="home",
            theme="general",
            keywords=("総合", "全体", "流れ"),
        ),
    )

    def list(
        self,
        category: str | None = None,
        theme: str | None = None,
    ) -> list[FortuneRuntimeDiscoveryItem]:
        items = list(self.ITEMS)

        if category is not None:
            items = [
                item
                for item in items
                if item.category == category
            ]

        if theme is not None:
            items = [
                item
                for item in items
                if item.theme == theme
            ]

        return items

    def search(
        self,
        query: str,
    ) -> list[FortuneRuntimeDiscoveryItem]:
        normalized = query.strip().lower()

        if not normalized:
            return list(self.ITEMS)

        result: list[FortuneRuntimeDiscoveryItem] = []

        for item in self.ITEMS:
            haystack = " ".join(
                (
                    item.key,
                    item.title,
                    item.description,
                    item.theme,
                    *item.keywords,
                )
            ).lower()

            if normalized in haystack:
                result.append(item)

        return result