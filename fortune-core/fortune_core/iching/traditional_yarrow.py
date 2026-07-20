from __future__ import annotations

import random

from dataclasses import dataclass


# ==========================================================
# Data Classes
# ==========================================================

@dataclass(slots=True)
class TraditionalChange:
    """
    一変（四営）の記録
    """

    before: int

    after: int

    left: int

    right: int

    removed: int

    left_remainder: int

    right_remainder: int


@dataclass(slots=True)
class TraditionalThrow:
    """
    一爻生成結果
    """

    line: int

    remaining_stems: int

    changes: list[TraditionalChange]

@dataclass(slots=True)
class TraditionalHexagram:
    """
    六爻生成結果
    """

    numbers: list[int]

    throws: list[TraditionalThrow]

# ==========================================================
# Traditional Yarrow Method
# ==========================================================

class TraditionalYarrowMethod:
    """
    本格筮竹法（四営十八変）

    Part1

        ・49本開始
        ・掛一
        ・分二
        ・揲四
        ・一変

    Part2

        ・三変

    Part3

        ・十八変

    """

    STEMS = 49

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

        left = random.randint(
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
        四営の一変。
        """

        before = stems

        # 掛一
        stems = self.remove_one(stems)

        # 分二
        left, right = self.divide(stems)

        # 右手から一本を掛ける
        right -= 1

        # 揲四
        left_rem = self.count_by_four(left)
        right_rem = self.count_by_four(right)

        removed = (
            1
            + left_rem
            + right_rem
        )

        stems -= removed

        change = TraditionalChange(
            before=before,
            after=stems,
            left=left,
            right=right,
            removed=removed,
            left_remainder=left_rem,
            right_remainder=right_rem,
        )

        return stems, change

    # ------------------------------------------------------
    # 三変
    # ------------------------------------------------------

    def three_changes(
        self,
    ) -> tuple[int, list[TraditionalChange]]:
        """
        三変を行い、
        残った蓍草本数を返す。
        """

        stems = self.initialize()

        history: list[TraditionalChange] = []

        for _ in range(3):

            stems, change = self.one_change(
                stems
            )

            history.append(change)

        return stems, history    

    # ------------------------------------------------------
    # 一爻
    # ------------------------------------------------------

    def cast_once(
        self,
    ) -> TraditionalThrow:
        """
        三変を行い、
        1本の爻を生成する。
        """

        stems, history = self.three_changes()

        value = stems // 4

        #
        # 24・28・32・36
        # ↓
        # 6・7・8・9
        #
        mapping = {

            6: 6,      # 老陰

            7: 7,      # 少陽

            8: 8,      # 少陰

            9: 9,      # 老陽

        }

        if value not in mapping:

            raise ValueError(

                f"Unexpected value: {value}"

            )

        return TraditionalThrow(

            line=mapping[value],

            remaining_stems=stems,

            changes=history,

        )
    # ------------------------------------------------------
    # 六爻
    # ------------------------------------------------------

    def cast(
        self,
    ):
        """
        Part3で実装
        """

        raise NotImplementedError(
            "Part3"
        )
    