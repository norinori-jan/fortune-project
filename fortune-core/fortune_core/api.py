from __future__ import annotations

from dataclasses import dataclass

from .iching import FortuneEngine


# ==========================================================
# API Request
# ==========================================================

@dataclass(frozen=True, slots=True)
class IChingRequest:
    """
    易経APIリクエスト
    """

    question: str

    method: str = "coin"


# ==========================================================
# API
# ==========================================================

class IChingAPI:
    """
    易経API

    FortuneEngine の公開インターフェース。
    """

    def __init__(
        self,
    ) -> None:

        self.engine = FortuneEngine()

    # ------------------------------------------------------
    # 占う
    # ------------------------------------------------------

    def divine(
        self,
        request: IChingRequest,
    ):
        """
        易占を実行する。
        """

        return self.engine.divine(

            question=request.question,

            method=request.method,

        )

    # ------------------------------------------------------
    # Coin
    # ------------------------------------------------------

    def coin(
        self,
        question: str,
    ):

        return self.engine.divine(

            question=question,

            method="coin",

        )

    # ------------------------------------------------------
    # Simple Yarrow
    # ------------------------------------------------------

    def simple_yarrow(
        self,
        question: str,
    ):

        return self.engine.divine(

            question=question,

            method="simple_yarrow",

        )

    # ------------------------------------------------------
    # Traditional Yarrow
    # ------------------------------------------------------

    def traditional_yarrow(
        self,
        question: str,
    ):

        return self.engine.divine(

            question=question,

            method="traditional_yarrow",

        )


# ==========================================================
# Singleton
# ==========================================================

api = IChingAPI()


__all__ = [

    "IChingRequest",

    "IChingAPI",

    "api",

]