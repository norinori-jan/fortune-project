from __future__ import annotations
from fortune_core.models.fortune_catalog import (
    FortuneCatalogItem,
)
class FortuneCatalogService:
    SYSTEMS = (
        FortuneCatalogItem(
            key="unified",
            name="総合占い",
            description="複数のテーマをまとめて確認します。",
            category="core",
        ),
        FortuneCatalogItem(
            key="tarot",
            name="タロット",
            description="カードの象徴からテーマを読み解きます。",
            category="divination",
        ),
        FortuneCatalogItem(
            key="meihua",
            name="梅花易数",
            description="卦の構成から変化の流れを読み解きます。",
            category="divination",
        ),
        FortuneCatalogItem(
            key="five-elements",
            name="五行",
            description="五行のバランスをテーマとして確認します。",
            category="analysis",
        ),
        FortuneCatalogItem(
            key="shichu",
            name="四柱",
            description="生年月日を基にしたプロフィール情報を確認します。",
            category="profile",
        ),
    )
    THEMES = (
        FortuneCatalogItem(
            key="general",
            name="総合",
            description="全体的な流れを確認します。",
            category="theme",
        ),
        FortuneCatalogItem(
            key="love",
            name="恋愛・人間関係",
            description="人とのつながりをテーマにします。",
            category="theme",
        ),
        FortuneCatalogItem(
            key="work",
            name="仕事",
            description="仕事や活動をテーマにします。",
            category="theme",
        ),
        FortuneCatalogItem(
            key="money",
            name="お金",
            description="計画や資源管理をテーマにします。",
            category="theme",
        ),
        FortuneCatalogItem(
            key="health",
            name="生活",
            description="生活リズムや日常をテーマにします。",
            category="theme",
        ),
    )
    def systems(self) -> tuple[FortuneCatalogItem, ...]:
        return self.SYSTEMS
    def themes(self) -> tuple[FortuneCatalogItem, ...]:
        return self.THEMES
    def all(self) -> tuple[FortuneCatalogItem, ...]:
        return self.SYSTEMS + self.THEMES