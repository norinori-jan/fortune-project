from __future__ import annotations
import hashlib
from fortune_core.models.compatibility import CompatibilityResult
class CompatibilityService:
    def build(
        self,
        person_a: str,
        person_b: str,
        theme: str = "general",
    ) -> CompatibilityResult:
        seed = f"{person_a}|{person_b}|{theme}"
        digest = hashlib.sha256(
            seed.encode("utf-8")
        ).digest()
        score = 50 + digest[0] % 51
        if score >= 85:
            title = "調和を育てやすい組み合わせ"
            message = "互いの違いを活かしながら関係を築きやすい流れです。"
            advice = "相手の考えを一度受け止めてから、自分の意見を伝えましょう。"
        elif score >= 70:
            title = "安定した関係を作りやすい組み合わせ"
            message = "共通点を意識すると自然なコミュニケーションにつながります。"
            advice = "無理に合わせるより、共通する目的を見つけましょう。"
        elif score >= 60:
            title = "理解を深めることがテーマ"
            message = "違いを知ることで関係性が見えやすくなります。"
            advice = "判断を急がず、相手の背景を確認してみましょう。"
        else:
            title = "ペースを整えることがテーマ"
            message = "それぞれの時間や考え方を尊重することが大切です。"
            advice = "距離を詰めすぎず、自然なペースを意識しましょう。"
        keywords = (
            ("調和", "理解", "信頼")
            if score >= 75
            else ("対話", "理解", "調整")
        )
        return CompatibilityResult(
            score=score,
            title=title,
            message=message,
            advice=advice,
            keywords=keywords,
        )