# fortune_core/report/models.py

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class PaperReport:
    """
    鑑定書全体を保持するモデル

    Engine.generate() → Chart
                     ↓
              PaperBuilder.build()
                     ↓
               PaperReport
    """

    # 命式
    chart: Any

    # 五行分析
    element_strength: Any

    # 格局
    kakukyoku: Any

    # 用神・喜神・忌神
    yojin: Any

    # 宮位
    house_gods: Any

    # 合・冲・刑・害・三合・方合など
    combinations: Any

    # 大運
    taiun: Any

    # 流年
    ryunen: Any

    # 流月
    ryugetsu: Any

    # 流日
    ryunichi: Any

    # AI鑑定
    ai_reading: Any