from __future__ import annotations
from dataclasses import dataclass
from hashlib import sha256
from fortune_core.models import FortuneItem, UnifiedFortune
@dataclass(frozen=True, slots=True)
class FortuneTheme:
    key: str
    title: str
    message: str
    advice: tuple[str, ...]
THEMES = (
    FortuneTheme(
        key="growth",
        title="成長",
        message="今は小さな変化を積み重ねることで、次の段階へ進みやすい時期です。",
        advice=(
            "今日できる小さな一歩を決める",
            "結果より継続を大切にする",
            "新しい情報を一つ取り入れる",
        ),
    ),
    FortuneTheme(
        key="connection",
        title="縁",
        message="人とのつながりや会話の中に、次の展開につながるヒントが生まれやすい時です。",
        advice=(
            "気になっている人へ一度連絡する",
            "相手の話を最後まで聞く",
            "一人で決めず意見を取り入れる",
        ),
    ),
    FortuneTheme(
        key="change",
        title="変化",
        message="これまでの方法に新しいやり方を加えることで、流れを変えられる時です。",
        advice=(
            "一つだけ方法を変えてみる",
            "不要なものを一つ手放す",
            "新しい選択肢を比較する",
        ),
    ),
    FortuneTheme(
        key="stability",
        title="安定",
        message="急いで結論を出すより、基礎を整えることで長く続く成果につながります。",
        advice=(
            "生活や仕事の基礎を整える",
            "予定に余白を作る",
            "確実にできることから進める",
        ),
    ),
    FortuneTheme(
        key="discovery",
        title="発見",
        message="今まで気づかなかった可能性が見つかりやすい時です。偶然の情報も大切にしてください。",
        advice=(
            "普段見ない情報に触れる",
            "疑問を一つ深掘りする",
            "偶然の出会いを記録する",
        ),
    ),
)
class UnifiedFortuneService:
    """
    既存の占術エンジンに依存しない、新規の総合占いサービス。
    後から I Ching / Tarot / 梅花 / 四柱推命などの
    実データを FortuneItem として接続できる。
    """
    def divine(
        self,
        question: str,
        theme: str = "general",
    ) -> UnifiedFortune:
        normalized = question.strip()
        if not normalized:
            raise ValueError("question must not be empty")
        selected = self._select_theme(normalized, theme)
        items = [
            FortuneItem(
                system="unified",
                title=selected.title,
                summary=selected.message,
                details={
                    "theme": selected.key,
                },
            )
        ]
        return UnifiedFortune(
            question=normalized,
            theme=selected.key,
            overall=selected.title,
            message=selected.message,
            items=items,
            keywords=self._keywords(selected),
            advice=list(selected.advice),
        )
    def _select_theme(
        self,
        question: str,
        requested_theme: str,
    ) -> FortuneTheme:
        if requested_theme and requested_theme != "general":
            for theme in THEMES:
                if theme.key == requested_theme:
                    return theme
        digest = sha256(question.encode("utf-8")).digest()
        index = int.from_bytes(digest[:4], "big") % len(THEMES)
        return THEMES[index]
    @staticmethod
    def _keywords(theme: FortuneTheme) -> list[str]:
        keyword_map = {
            "growth": ["成長", "継続", "前進"],
            "connection": ["縁", "対話", "協力"],
            "change": ["変化", "挑戦", "転換"],
            "stability": ["安定", "基礎", "継続"],
            "discovery": ["発見", "可能性", "学び"],
        }
        return keyword_map.get(theme.key, [])