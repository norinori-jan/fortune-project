from __future__ import annotations
from datetime import date
import hashlib
from fortune_core.models.fortune_profile import FortuneProfile
class FortuneProfileService:
    KEYWORDS = (
        "前進",
        "調和",
        "発見",
        "成長",
        "安定",
        "変化",
        "直感",
        "整理",
    )
    def build(
        self,
        nickname: str,
        birth_date: date | None = None,
        favorite_system: str = "unified",
        favorite_theme: str = "general",
    ) -> FortuneProfile:
        raw = "|".join(
            (
                nickname,
                birth_date.isoformat() if birth_date else "",
                favorite_system,
                favorite_theme,
            )
        )
        digest = hashlib.sha256(raw.encode("utf-8")).digest()
        keywords = tuple(
            self.KEYWORDS[
                digest[index] % len(self.KEYWORDS)
            ]
            for index in range(3)
        )
        profile_id = hashlib.sha256(
            raw.encode("utf-8")
        ).hexdigest()[:16]
        return FortuneProfile(
            profile_id=profile_id,
            nickname=nickname,
            birth_date=(
                birth_date.isoformat()
                if birth_date
                else None
            ),
            favorite_system=favorite_system,
            favorite_theme=favorite_theme,
            keywords=keywords,
        )
    def create(self, birth_date: "str | date | None" = None, nickname: str = "あなた") -> FortuneProfile:
        """Hub から呼ばれる入口。生年月日は文字列（YYYY-MM-DD）でも日付でもよい。"""
        if isinstance(birth_date, str) and birth_date:
            birth_date = date.fromisoformat(birth_date)
        return self.build(nickname=nickname, birth_date=birth_date or None)
