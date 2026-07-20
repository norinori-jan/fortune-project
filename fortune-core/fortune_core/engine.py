from __future__ import annotations

from dataclasses import dataclass

from .iching.coin_method import CoinMethod
from .iching.hexagrams import (
    HexagramEngine,
    HexagramResult,
)
from .iching.interpretation import (
    InterpretationEngine,
    ReadingResult,
)
from .iching.traditional_yarrow import (
    TraditionalYarrowMethod,
)


@dataclass(slots=True)
class FortuneReading:
    """
    FortuneEngine が返す統合結果
    """

    hexagram: HexagramResult

    reading: ReadingResult


class FortuneEngine:
    """
    易経統合エンジン

    ・コイン法
    ・筮竹法
    ・卦生成
    ・解釈生成

    をまとめて扱う。
    """

    def __init__(self) -> None:

        self.hexagrams = HexagramEngine()

        self.interpreter = InterpretationEngine()

    # ---------------------------------------------------------
    # コイン法
    # ---------------------------------------------------------

    def cast_coin(
        self,
    ) -> FortuneReading:
        """
        コイン法で占う。
        """

        method = CoinMethod()

        numbers = method.cast()

        result = self.hexagrams.generate(
            numbers
        )

        reading = self.interpreter.interpret(
            result
        )

        return FortuneReading(
            hexagram=result,
            reading=reading,
        )

    # ---------------------------------------------------------
    # 筮竹法
    # ---------------------------------------------------------

    def cast_yarrow(
        self,
    ) -> FortuneReading:
        """
        本格筮竹法で占う。
        """

        method = TraditionalYarrowMethod()

        throw = method.cast()

        result = self.hexagrams.generate(
            throw.numbers
        )

        reading = self.interpreter.interpret(
            result
        )

        return FortuneReading(
            hexagram=result,
            reading=reading,
        )

    # ---------------------------------------------------------
    # 任意の爻で生成
    # ---------------------------------------------------------

    def from_numbers(
        self,
        numbers: list[int],
    ) -> FortuneReading:
        """
        爻値から占断する。
        """

        result = self.hexagrams.generate(
            numbers
        )

        reading = self.interpreter.interpret(
            result
        )

        return FortuneReading(
            hexagram=result,
            reading=reading,
        )