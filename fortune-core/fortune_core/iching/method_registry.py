from __future__ import annotations

from .coin_method import CoinMethod
from .yarrow_method import SimpleYarrowMethod
from .traditional_yarrow import TraditionalYarrowMethod


class MethodRegistry:
    def __init__(self) -> None:
        self._methods = {
            "coin": CoinMethod(),
            "simple_yarrow": SimpleYarrowMethod(),
            "traditional_yarrow": TraditionalYarrowMethod(),
        }

    def get(self, name: str):
        try:
            return self._methods[name]
        except KeyError as exc:
            raise ValueError(f"Unknown method: {name}") from exc

    def names(self) -> list[str]:
        return list(self._methods.keys())