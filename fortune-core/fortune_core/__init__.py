"""
fortune_core
占術共通ライブラリ
"""

__version__ = "0.1.0"

from .iching import FortuneEngine
from .iching import FortuneResult

__all__ = [
    "FortuneEngine",
    "FortuneResult",
]
