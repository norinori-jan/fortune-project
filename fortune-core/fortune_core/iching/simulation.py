from __future__ import annotations

from collections import Counter

from .traditional_yarrow import TraditionalYarrowMethod


class YarrowSimulation:
    """
    筮竹法シミュレーション

    TraditionalYarrowMethod を大量実行し、
    爻値(6,7,8,9)の分布を確認する。
    """

    def __init__(
        self,
        seed: int | None = None,
    ) -> None:

        self.method = TraditionalYarrowMethod(seed=seed)

    # ---------------------------------------------------------
    # 一爻シミュレーション
    # ---------------------------------------------------------

    def simulate_lines(
        self,
        count: int = 100000,
    ) -> dict:

        counter = Counter()

        for _ in range(count):

            throw = self.method.cast_once()

            counter[throw.line] += 1

        result = {}

        for line in (6, 7, 8, 9):

            n = counter[line]

            result[line] = {
                "count": n,
                "ratio": n / count,
                "percent": round(n / count * 100, 4),
            }

        return result

    # ---------------------------------------------------------
    # 表示
    # ---------------------------------------------------------

    def print_report(
        self,
        count: int = 100000,
    ) -> None:

        result = self.simulate_lines(count)

        print()
        print("=" * 50)
        print("Traditional Yarrow Simulation")
        print("=" * 50)
        print(f"Trials : {count}")
        print()

        for line in (6, 7, 8, 9):

            data = result[line]

            print(
                f"{line} : "
                f"{data['count']:>7}  "
                f"{data['percent']:>7.3f}%"
            )

        print()