from __future__ import annotations
from typing import Any, Protocol, runtime_checkable


@runtime_checkable
class FortuneProvider(Protocol):
    """占術プロバイダの最小インターフェース。

    実行側（FortuneRunner）は divine / draw / analyze のいずれかを呼ぶ。
    ここでは型の目印だけを定義する（このファイルは取り込み時に欠けていたため再作成）。
    """

    def divine(self, *args: Any, **kwargs: Any) -> Any:  # pragma: no cover
        ...
