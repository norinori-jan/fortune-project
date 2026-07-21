from __future__ import annotations

import random

from dataclasses import dataclass

from .yarrow_method import BaseYarrowMethod


# ==========================================================
# Data Classes
# ==========================================================

@dataclass(slots=True)
class TraditionalChange:
    """
    四営一変
    """

    before: int

    after: int

    left: int

    right: int

    human: int

    left_remainder: int

    right_remainder: int

    removed: int


@dataclass(slots=True)
class TraditionalThrow:
    """
    一爻生成結果
    """

    line: int

    remaining_stems: int

    changes: list[TraditionalChange]

    initial_stems: int = 49


@dataclass(slots=True)
class TraditionalHexagram:
    """
    六爻生成結果
    """

    method: str

    numbers: list[int]

    throws: list[TraditionalThrow]


# ==========================================================
# Traditional Yarrow Method
# ==========================================================

class TraditionalYarrowMethod(BaseYarrowMethod):
    """
    本格筮竹法（四営十八変）
    """

    STEMS = 49

    def __init__(
        self,
        seed: int | None = None,
    ) -> None:
        """
        Parameters
        ----------
        seed:
            乱数シード。
            指定すると同じ結果を再現できる。
        """

        self.random = random.Random(seed)

    # ------------------------------------------------------
    # 占法名
    # ------------------------------------------------------

    def method_name(
        self,
    ) -> str:

        return "traditional_yarrow"

    # ------------------------------------------------------
    # 初期化
    # ------------------------------------------------------

    def initialize(
        self,
    ) -> int:
        """
        蓍草49本を用意する。
        """

        return self.STEMS

    # ------------------------------------------------------
    # 掛一
    # ------------------------------------------------------

    def remove_one(
        self,
        stems: int,
    ) -> int:
        """
        掛一

        一本を天地人の象徴として取り除く。
        """

        return stems - 1

    # ------------------------------------------------------
    # 分二
    # ------------------------------------------------------

    def divide(
        self,
        stems: int,
    ) -> tuple[int, int]:
        """
        左右へランダムに分ける。
        """

        left = self.random.randint(
            1,
            stems - 1,
        )

        right = stems - left

        return left, right

    # ------------------------------------------------------
    # 揲四
    # ------------------------------------------------------

    def count_by_four(
        self,
        value: int,
    ) -> int:
        """
        四本ずつ数えた余り。

        余り0は4とする。
        """

        remainder = value % 4

        if remainder == 0:
            return 4

        return remainder
    # ------------------------------------------------------
    # 一変（四営）
    # ------------------------------------------------------

    def one_change(
        self,
        stems: int,
    ) -> tuple[int, TraditionalChange]:
        """
        四営一変
        """

        before = stems

        # 掛一
        stems -= 1

        human = 1

        # 分二
        left, right = self.divide(stems)

        # 右から一本
        right -= 1

        left_rem = self.count_by_four(left)

        right_rem = self.count_by_four(right)

        removed = (

            human

            + left_rem

            + right_rem

        )

        stems -= removed

        change = TraditionalChange(

            before=before,

            after=stems,

            left=left,

            right=right,

            human=human,

            left_remainder=left_rem,

            right_remainder=right_rem,

            removed=removed,

        )

        return stems, change

    # ------------------------------------------------------
    # 三変
    # ------------------------------------------------------

    def three_changes(
        self,
    ) -> tuple[int, list[TraditionalChange]]:
        """
        三変（四営×3）

        Returns
        -------
        (
            最終残本数,
            各変の詳細
        )
        """

        stems = self.initialize()

        history: list[TraditionalChange] = []

        # 第一変
        stems, change = self.one_change(stems)
        history.append(change)

        # 第二変
        stems, change = self.one_change(stems)
        history.append(change)

        # 第三変
        stems, change = self.one_change(stems)
        history.append(change)

        return stems, history

    # ------------------------------------------------------
    # 爻値計算
    # ------------------------------------------------------

    def calculate_line(
        self,
        remaining_stems: int,
    ) -> int:
        """
        残り蓍草本数から
        爻値（6・7・8・9）へ変換する。
        """

        value = remaining_stems // 4

        mapping = {

            6: 6,

            7: 7,

            8: 8,

            9: 9,

        }

        if value not in mapping:

            raise ValueError(

                f"Unexpected value: {value}"

            )

        return mapping[value]
    # ------------------------------------------------------
    # 一爻生成
    # ------------------------------------------------------

    def cast_once(
        self,
    ) -> TraditionalThrow:
        """
        三変を行い、
        1本の爻を生成する。
        """

        stems, history = self.three_changes()

        line = self.calculate_line(
            stems
        )

        return TraditionalThrow(

            line=line,

            remaining_stems=stems,

            changes=history,

        )

    # ------------------------------------------------------
    # 六爻生成
    # ------------------------------------------------------

    def cast(
        self,
    ) -> TraditionalHexagram:
        """
        六本の爻を生成する。

        Returns
        -------
        TraditionalHexagram
        """

        throws: list[TraditionalThrow] = []

        numbers: list[int] = []

        for _ in range(6):

            throw = self.cast_once()

            throws.append(throw)

            numbers.append(throw.line)

        return TraditionalHexagram(

            method=self.method_name(),

            numbers=numbers,

            throws=throws,

        )

    # ------------------------------------------------------
    # 複数回実行
    # ------------------------------------------------------

    def cast_many(
        self,
        count: int,
    ) -> list[TraditionalHexagram]:
        """
        六爻生成を複数回行う。

        Parameters
        ----------
        count:
            実行回数

        Returns
        -------
        list[TraditionalHexagram]
        """

        if count < 1:
            raise ValueError(
                "count は1以上を指定してください。"
            )

        return [

            self.cast()

            for _ in range(count)

        ]


__all__ = [

    "TraditionalChange",

    "TraditionalThrow",

    "TraditionalHexagram",

    "TraditionalYarrowMethod",

]