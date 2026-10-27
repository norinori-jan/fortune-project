from __future__ import annotations
from dataclasses import dataclass
@dataclass(frozen=True, slots=True)
class FortuneTheme:
    key: str
    title: str
    keywords: tuple[str, ...]
    message: str
    advice: tuple[str, ...]
THEMES = {
    "love": FortuneTheme(
        key="love",
        title="恋愛運",
        keywords=("縁", "対話", "信頼"),
        message="相手との距離を急いで縮めるより、自然な対話を重ねることが流れを整えます。",
        advice=(
            "相手の言葉をよく聞く",
            "自分の気持ちを整理する",
            "無理に答えを急がない",
        ),
    ),
    "work": FortuneTheme(
        key="work",
        title="仕事運",
        keywords=("集中", "計画", "成果"),
        message="目標を細かく分けて、一つずつ処理することが成果につながります。",
        advice=(
            "最優先事項を一つ決める",
            "作業を小さく分ける",
            "完成したものを記録する",
        ),
    ),
    "money": FortuneTheme(
        key="money",
        title="金運",
        keywords=("管理", "蓄積", "選択"),
        message="大きな変化を急ぐより、日々のお金の流れを把握することが重要です。",
        advice=(
            "支出を確認する",
            "必要なものと欲しいものを分ける",
            "長期的な計画を立てる",
        ),
    ),
    "health": FortuneTheme(
        key="health",
        title="健康運",
        keywords=("休息", "習慣", "調整"),
        message="無理を重ねるより、生活リズムを整えることを優先してください。",
        advice=(
            "休息時間を確保する",
            "生活リズムを確認する",
            "無理な予定を減らす",
        ),
    ),
    "general": FortuneTheme(
        key="general",
        title="総合運",
        keywords=("流れ", "選択", "成長"),
        message="目の前の状況を整理し、小さな行動から流れを作っていく時です。",
        advice=(
            "今日できることを一つ決める",
            "不要なことを一つ減らす",
            "次の一歩を具体化する",
        ),
    ),
}
class FortuneThemeService:
    def get(self, key: str) -> FortuneTheme:
        return THEMES.get(
            key.strip().lower(),
            THEMES["general"],
        )
    def all(self) -> list[FortuneTheme]:
        return list(THEMES.values())
