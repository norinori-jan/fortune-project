from __future__ import annotations
from fortune_core.models.question_suggestion import QuestionSuggestion
class QuestionSuggestionService:
    QUESTIONS = {
        "love": (
            (
                "今の人間関係で意識したいことは？",
                "unified",
                "人間関係全体の流れを確認する",
            ),
            (
                "これからの出会いについて知りたい",
                "tarot",
                "カードから象徴的なテーマを見る",
            ),
        ),
        "work": (
            (
                "仕事で次に取り組むべきことは？",
                "unified",
                "現在の流れを整理する",
            ),
            (
                "仕事上の変化をどう受け止めるべき？",
                "tarot",
                "変化を象徴として読む",
            ),
        ),
        "money": (
            (
                "お金について今意識したいことは？",
                "unified",
                "金運に関するテーマを整理する",
            ),
            (
                "今後の計画を見直すポイントは？",
                "meihua",
                "変化と状況の流れを見る",
            ),
        ),
        "health": (
            (
                "生活リズムで見直したいことは？",
                "unified",
                "日常のバランスを考える",
            ),
        ),
        "general": (
            (
                "今日の全体運を知りたい",
                "unified",
                "今日の流れを見る",
            ),
            (
                "今の自分に必要なメッセージは？",
                "tarot",
                "カードから象徴的なメッセージを見る",
            ),
            (
                "これからの流れを知りたい",
                "meihua",
                "変化の方向性を考える",
            ),
        ),
    }
    def suggest(
        self,
        theme: str = "general",
    ) -> tuple[QuestionSuggestion, ...]:
        items = self.QUESTIONS.get(
            theme,
            self.QUESTIONS["general"],
        )
        return tuple(
            QuestionSuggestion(
                question=question,
                theme=theme,
                system=system,
                reason=reason,
            )
            for question, system, reason in items
        )