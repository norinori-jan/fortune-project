from __future__ import annotations

from dataclasses import dataclass

from .coin_method import CoinMethod
from .yarrow_method import SimpleYarrowMethod
from .traditional_yarrow import TraditionalYarrowMethod

from .hexagrams import (
    HexagramEngine,
    HexagramResult,
)

from .interpretation import (
    Interpretation,
    InterpretationEngine,
)


# ==========================================================
# Data Classes
# ==========================================================

@dataclass(frozen=True, slots=True)
class FortuneResult:
    """
    FortuneEngine の最終結果
    """

    question: str

    method: str

    hexagram: HexagramResult

    interpretation: Interpretation


# ==========================================================
# Fortune Engine
# ==========================================================

class FortuneEngine:
    """
    易経統合エンジン

    全ての占法・卦生成・解釈を統括する。
    """

    def __init__(
        self,
    ) -> None:

        self.hexagram_engine = HexagramEngine()

        self.interpretation_engine = InterpretationEngine()

        self.methods = {

            "coin": CoinMethod(),

            "simple_yarrow": SimpleYarrowMethod(),

            "traditional_yarrow": TraditionalYarrowMethod(),

        }

    # ------------------------------------------------------
    # 利用可能な占法
    # ------------------------------------------------------

    def available_methods(
        self,
    ) -> list[str]:
        """
        利用可能な占法一覧を返す。
        """

        return list(
            self.methods.keys()
        )

    # ------------------------------------------------------
    # 占法取得
    # ------------------------------------------------------

    def get_method(
        self,
        name: str,
    ):
        """
        占法オブジェクト取得
        """

        try:

            return self.methods[name]

        except KeyError as exc:

            raise ValueError(
                f"Unknown method: {name}"
            ) from exc

    # ------------------------------------------------------
    # 占う
    # ------------------------------------------------------

    def divine(
        self,
        question: str,
        method: str = "coin",
    ) -> FortuneResult:
        """
        易占を実行する。

        Parameters
        ----------
        question:
            質問内容

        method:
            coin
            simple_yarrow
            traditional_yarrow

        Returns
        -------
        FortuneResult
        """

        casting_method = self.get_method(
            method
        )

        hexagram = casting_method.generate(
            self.hexagram_engine
        )

        interpretation = (
            self.interpretation_engine.interpret(
                hexagram
            )
        )

        return FortuneResult(

            question=question,

            method=method,

            hexagram=hexagram,

            interpretation=interpretation,

        )

    # ------------------------------------------------------
    # Coin Method
    # ------------------------------------------------------

    def divine_by_coin(
        self,
        question: str,
    ) -> FortuneResult:
        """
        三枚銭法で占う。
        """

        return self.divine(

            question=question,

            method="coin",

        )

    # ------------------------------------------------------
    # Simple Yarrow
    # ------------------------------------------------------

    def divine_by_simple_yarrow(
        self,
        question: str,
    ) -> FortuneResult:
        """
        簡易筮竹法で占う。
        """

        return self.divine(

            question=question,

            method="simple_yarrow",

        )

    # ------------------------------------------------------
    # Traditional Yarrow
    # ------------------------------------------------------

    def divine_by_traditional_yarrow(
        self,
        question: str,
    ) -> FortuneResult:
        """
        本格筮竹法で占う。
        """

        return self.divine(

            question=question,

            method="traditional_yarrow",

        )


__all__ = [

    "FortuneEngine",

    "FortuneResult",

]