from .dashboard_fortune import FortuneDashboardService
__all__ = ["FortuneDashboardService"]

# [貼り付けメモ] fortune-core/fortune_core/models/__init__.py への追加用新規互換ファイル

# [貼り付けメモ] 既存ファイルを変更せず、まとめて扱える別名モジュールを追加します。

# [貼り付けメモ] fortune-core/fortune_core/dashboard_models.py

from fortune_core.models.dashboard import DashboardCard, FortuneDashboard
__all__ = [
    "DashboardCard",
    "FortuneDashboard",
]
