from __future__ import annotations

import random

from abc import ABC
from abc import abstractmethod

from dataclasses import dataclass


# =========================================================
# Data Classes
# =========================================================

class TraditionalYarrowMethod(BaseYarrowMethod):
    """
    本格筮竹法（四営十八変）

    蓍草49本を用いて
    三変を1回の爻生成とする。

    Phase A
        ・蓍草初期化
        ・掛一
        ・分二
        ・揲四
    """

    STEMS = 49

    # ---------------------------------------------------------
    # 蓍草初期化
    # ---------------------------------------------------------

    def initialize_stems(self) -> int:
        """
        蓍草49本を用意する。
        """

        return self.STEMS

    # ---------------------------------------------------------
    # 掛一
    # ---------------------------------------------------------

    def remove_one(self, stems: int) -> int:
        """
        掛一

        1本を天地人の象徴として除く。
        """

        return stems - 1

    # ---------------------------------------------------------
    # 分二
    # ---------------------------------------------------------

    def divide_stems(
        self,
        stems: int,
    ) -> tuple[int, int]:
        """
        分二

        残りを左右にランダム分割する。
        """

        left = random.randint(
            1,
            stems - 1,
        )

        right = stems - left

        return left, right

    # ---------------------------------------------------------
    # 揲四
    # ---------------------------------------------------------

    def remainder_by_four(
        self,
        value: int,
    ) -> int:
        """
        4本ずつ数えた余り。

        余り0は4とする。
        """

        r = value % 4

        if r == 0:
            return 4

        return r

# ---------------------------------------------------------
# 一変（四営）
# ---------------------------------------------------------

def one_change(
    self,
    stems: int,
) -> tuple[int, dict]:
    """
    四営の一変を行う。

    Returns
    -------
    (remaining_stems, detail)
    """

    # 掛一（天地人）
    stems -= 1

    # 分二
    left = random.randint(1, stems - 1)
    right = stems - left

    # 右から一本を掛ける
    right -= 1

    # 揲四
    left_rem = left % 4
    right_rem = right % 4

    if left_rem == 0:
        left_rem = 4

    if right_rem == 0:
        right_rem = 4

    removed = 1 + left_rem + right_rem

    remaining = stems - removed

    detail = {

        "left": left,

        "right": right,

        "left_remainder": left_rem,

        "right_remainder": right_rem,

        "removed": removed,

        "remaining": remaining,

    }

    return remaining, detail
# ---------------------------------------------------------
# 一爻
# ---------------------------------------------------------

def cast_once(
    self,
) -> YarrowThrow:
    """
    三変を行い1本の爻を生成する。
    """

    stems = self.initialize_stems()

    # 第一変
    stems, _ = self.one_change(stems)

    # 第二変
    stems, _ = self.one_change(stems)

    # 第三変
    stems, _ = self.one_change(stems)

    # 残り本数から爻値へ変換
    value = stems // 4

    mapping = {
        6: 6,   # 老陰
        7: 7,   # 少陽
        8: 8,   # 少陰
        9: 9,   # 老陽
    }

    if value not in mapping:
        raise ValueError(
            f"Unexpected yarrow value: {value}"
        )

    return YarrowThrow(
        line=mapping[value]
    )

# =========================================================
# Simple
# =========================================================

class SimpleYarrowMethod(BaseYarrowMethod):
    """
    簡易筮竹法

    確率だけ筮竹法に合わせる。

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

    def cast_once(
        self,
    ) -> YarrowThrow:

        return YarrowThrow(

            line=random.choice(
                self.VALUES
            )

        )


# =========================================================
# Traditional
# =========================================================

class TraditionalYarrowMethod(BaseYarrowMethod):
    """
    本格筮竹法（四営十八変）

    現在は未実装。

    将来的に

        ・蓍草49本
        ・掛一
        ・分二
        ・掛一
        ・揲四
        ・三変
        ・十八変

    を実装する。
    """

    def cast_once(
        self,
    ) -> YarrowThrow:

        raise NotImplementedError(
            "TraditionalYarrowMethod は未実装です。"
        )