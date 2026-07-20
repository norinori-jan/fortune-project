from __future__ import annotations

import random

from dataclasses import dataclass


@dataclass(frozen=True)
class CoinThrow:
    """
    三枚銭法の1回の投擲結果

    coins:
        各コインの値
        表 = 3
        裏 = 2

    total:
        合計値（6〜9）

    line:
        易の爻

        6 = 老陰
        7 = 少陽
        8 = 少陰
        9 = 老陽
    """

    coins: list[int]

    total: int

    line: int


@dataclass(frozen=True)
class CoinCast:
    """
    三枚銭法による六爻完成結果
    """

    method: str

    throws: list[CoinThrow]

    numbers: list[int]


class CoinMethod:
    """
    三枚銭法

    コイン3枚を投げて1本の爻を生成する。

        表 = 3
        裏 = 2

    合計

        6 = 老陰（変陰）
        7 = 少陽（陽）
        8 = 少陰（陰）
        9 = 老陽（変陽）
    """

    HEAD = 3
    TAIL = 2

    # ---------------------------------------------------------
    # コイン1枚
    # ---------------------------------------------------------

    def toss_coin(self) -> int:
        """
        コイン1枚を投げる。

        Returns
        -------
        int
            表=3 または 裏=2
        """

        return random.choice(
            [
                self.HEAD,
                self.TAIL,
            ]
        )

    # ---------------------------------------------------------
    # 三枚投げる（1爻）
    # ---------------------------------------------------------

    def cast_once(self) -> CoinThrow:
        """
        三枚投げて1本の爻を生成する。
        """

        coins = [
            self.toss_coin()
            for _ in range(3)
        ]

        total = sum(coins)

        return CoinThrow(
            coins=coins,
            total=total,
            line=total,
        )

    # ---------------------------------------------------------
    # 六爻生成
    # ---------------------------------------------------------

    def cast(self) -> CoinCast:
        """
        六回投げて一卦を生成する。
        """

        throws = [
            self.cast_once()
            for _ in range(6)
        ]

        return CoinCast(
            method="coin",
            throws=throws,
            numbers=[
                throw.line
                for throw in throws
            ],
        )

    # ---------------------------------------------------------
    # 占う（HexagramEngine連携）
    # ---------------------------------------------------------

    def generate(self, engine):
        """
        HexagramEngine と連携して
        卦を生成する。

        Parameters
        ----------
        engine : HexagramEngine

        Returns
        -------
        HexagramResult
        """

        cast = self.cast()

        return engine.generate(
            cast.numbers
        )