from __future__ import annotations
import hashlib
from ..models.fortune_score import FortuneScore
class FortuneScoringService:
    """
    占術そのものの優劣ではなく、
    現在のテーマに対する表示上の強度を生成する。
    """
    LABELS = (
        (90, "とても強い"),
        (75, "強め"),
        (60, "良好"),
        (45, "標準"),
        (30, "控えめ"),
        (0, "静かな流れ"),
    )
    REASONS = {
        "general": "全体の流れを確認するテーマとして算出しました。",
        "love": "関係性を考えるテーマとして算出しました。",
        "work": "仕事や役割を考えるテーマとして算出しました。",
        "money": "お金や計画を考えるテーマとして算出しました。",
        "health": "生活バランスを考えるテーマとして算出しました。",
    }
    def score(
        self,
        *,
        system: str,
        theme: str = "general",
        question: str = "",
    ) -> FortuneScore:
        raw = (
            f"{system}|{theme}|{question}"
        ).encode("utf-8")
        digest = hashlib.sha256(raw).digest()
        value = 30 + (
            int.from_bytes(
                digest[:2],
                "big",
            )
            % 71
        )
        label = "標準"
        for threshold, current_label in self.LABELS:
            if value >= threshold:
                label = current_label
                break
        return FortuneScore(
            system=system,
            theme=theme,
            score=value,
            label=label,
            reason=self.REASONS.get(
                theme,
                self.REASONS["general"],
            ),
        )