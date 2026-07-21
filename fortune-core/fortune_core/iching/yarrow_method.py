from __future__ import annotations

import random

from abc import ABC
from abc import abstractmethod

from dataclasses import dataclass


# =========================================================
# Data Classes
# =========================================================

@dataclass(frozen=True, slots=True)
class YarrowThrow:
    """
    一爻生成結果

    line
        6 = 老陰
        7 = 少陽
        8 = 少陰
        9 = 老陽
    """

    line: int


@dataclass(frozen=True, slots=True)
class YarrowCast:
    """
    簡易筮竹法 六爻結果
    """

    method: str

    throws: list[YarrowThrow]

    numbers: list[int]


# =========================================================
# Base
# =========================================================

class BaseYarrowMethod(ABC):
    """
    筮竹法共通クラス

    CoinMethod と同じAPIを提供する。

        cast_once()

        cast()

        generate(engine)
    """

    @abstractmethod
    def cast_once(
        self,
    ) -> YarrowThrow:
        """
        一爻生成
        """
        raise NotImplementedError

    # ---------------------------------------------------------
    # 六爻生成
    # ---------------------------------------------------------

    def cast(
        self,
    ) -> YarrowCast:

        throws = [

            self.cast_once()

            for _ in range(6)

        ]

        return YarrowCast(

            method=self.method_name(),

            throws=throws,

            numbers=[

                throw.line

                for throw in throws

            ],
        )

    # ---------------------------------------------------------
    # Engine連携
    # ---------------------------------------------------------

    def generate(
        self,
        engine,
    ):

        cast = self.cast()

        return engine.generate(

            cast.numbers

        )

    # ---------------------------------------------------------
    # 名前
    # ---------------------------------------------------------

    @abstractmethod
    def method_name(
        self,
    ) -> str:

        raise NotImplementedError
# =========================================================
# Simple Yarrow Method
# =========================================================

class SimpleYarrowMethod(BaseYarrowMethod):
    """
    簡易筮竹法

    出現確率のみ本格筮竹法へ近づける。

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

    # ---------------------------------------------------------
    # 占法名
    # ---------------------------------------------------------

    def method_name(
        self,
    ) -> str:

        return "simple_yarrow"

    # ---------------------------------------------------------
    # 一爻生成
    # ---------------------------------------------------------

    def cast_once(
        self,
    ) -> YarrowThrow:

        return YarrowThrow(

            line=random.choice(
                self.VALUES
            )

        )

    # ---------------------------------------------------------
    # 複数回実行
    # ---------------------------------------------------------

    def cast_many(
        self,
        count: int,
    ) -> list[YarrowCast]:
        """
        六爻生成を複数回実行する。

        Parameters
        ----------
        count
            実行回数

        Returns
        -------
        list[YarrowCast]
        """

        if count < 1:
            raise ValueError(
                "count は1以上を指定してください。"
            )

        return [

            self.cast()

            for _ in range(count)

        ]    