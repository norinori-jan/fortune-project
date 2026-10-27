from __future__ import annotations
from datetime import date
import hashlib
from fortune_core.models.fortune_message import FortuneMessage
class FortuneMessageService:
    MESSAGES = (
        ("前進", "小さな一歩を大切にする日", "始める前に完璧を求めなくても大丈夫です。"),
        ("整理", "不要なものを手放す日", "一つ減らすことで、新しい余白が生まれます。"),
        ("調和", "人とのつながりを意識する日", "短い言葉でも気持ちを伝えてみましょう。"),
        ("発見", "新しい視点を探す日", "いつもと違う方法を一つ試してみましょう。"),
        ("成長", "積み重ねを確認する日", "昨日より少し進んだことに目を向けましょう。"),
        ("安定", "足元を整える日", "生活や予定を整理すると次の動きが見えてきます。"),
        ("変化", "流れを受け入れる日", "予定外の出来事にも柔軟に対応しましょう。"),
        ("直感", "自分の感覚を確認する日", "最初に感じたことをメモしてみましょう。"),
    )
    def build(
        self,
        question: str,
        target_date: date | None = None,
    ) -> FortuneMessage:
        target_date = target_date or date.today()
        digest = hashlib.sha256(
            f"{question}|{target_date.isoformat()}".encode("utf-8")
        ).digest()
        index = digest[0] % len(self.MESSAGES)
        keyword, title, message = self.MESSAGES[index]
        return FortuneMessage(
            message_id=digest.hex()[:16],
            category="daily",
            title=title,
            message=message,
            keyword=keyword,
        )