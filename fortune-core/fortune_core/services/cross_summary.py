from __future__ import annotations
from collections import Counter
from typing import Iterable
from ..models.cross_summary import CrossSummary
from ..models.fortune_result import FortuneResult
class FortuneCrossSummaryService:
    HEADLINES = {
        "general": "今の全体テーマ",
        "love": "今の関係性テーマ",
        "work": "今の仕事テーマ",
        "money": "今のお金のテーマ",
        "health": "今の生活テーマ",
    }
    def summarize(
        self,
        *,
        theme: str,
        results: Iterable[FortuneResult],
    ) -> CrossSummary:
        items = list(results)
        systems = tuple(
            dict.fromkeys(
                item.system
                for item in items
            )
        )
        counter: Counter[str] = Counter()
        for item in items:
            counter.update(item.keywords)
        common_keywords = tuple(
            keyword
            for keyword, _ in counter.most_common(5)
        )
        scores = {
            item.system: item.score
            for item in items
            if item.score is not None
        }
        if common_keywords:
            keyword_text = "・".join(common_keywords[:3])
            message = (
                f"複数の結果から「{keyword_text}」が"
                "共通テーマとして見つかりました。"
            )
        else:
            message = (
                "複数の占術結果を並べて、"
                "共通するテーマを確認できます。"
            )
        return CrossSummary(
            theme=theme,
            headline=self.HEADLINES.get(
                theme,
                self.HEADLINES["general"],
            ),
            message=message,
            common_keywords=common_keywords,
            systems=systems,
            scores=scores,
        )
