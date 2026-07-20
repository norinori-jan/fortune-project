from __future__ import annotations

import random

from dataclasses import dataclass


@dataclass(frozen=True)
class CastResult:
    """
    占筮結果

    numbers:
        6 = 老陰
        7 = 少陽
        8 = 少陰
        9 = 老陽
    """

    method: str

    numbers: list[int]


class CoinMethod:
    """
    三枚銭法

    表 = 3
    裏 = 2

    合計

        6 = 老陰
        7 = 少陽
        8 = 少陰
        9 = 老陽
    """

    def cast_once(self) -> int:

        total = sum(

            random.choice([2, 3])

            for _ in range(3)

        )

        return total

    def cast(self) -> CastResult:

        return CastResult(

            method="coin",

            numbers=[

                self.cast_once()

                for _ in range(6)

            ],
        )


class YarrowMethod:
    """
    筮竹法（簡易版）

    本実装では
    出現確率のみ筮竹法に近づける。

        6 : 1
        7 : 5
        8 : 7
        9 : 3
    """

    VALUES = [

        6,

        7, 7, 7, 7, 7,

        8, 8, 8, 8, 8, 8, 8,

        9, 9, 9,

    ]

    def cast_once(self) -> int:

        return random.choice(self.VALUES)

    def cast(self) -> CastResult:

        return CastResult(

            method="yarrow",

            numbers=[

                self.cast_once()

                for _ in range(6)

            ],
        )