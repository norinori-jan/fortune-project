# fortune_core/shichu/calendar.py
from datetime import datetime, timedelta
import json


class ShichuCalendar:
    """
    四柱推命の暦計算を担当するクラス。
    - 経度補正（任意）
    - 節入り（立春・啓蟄・清明…）による年柱・月柱の切り替え
    - 日柱（六十干支）の計算
    - 時柱（十二支）の計算
    """

    # ------------------------------------------------------------
    # 経度補正テーブル（日本主要都市）
    # ------------------------------------------------------------
    LONGITUDE = {
        "tokyo": 18,
        "osaka": 2,
        "nagoya": 8,
        "sendai": 20,
        "sapporo": 25,
        "hiroshima": -6,
        "fukuoka": -18,
        "naha": -29
    }

    def __init__(self, solar_terms_json_path: str):
        """
        solar_terms.json を読み込む。
        形式：
        {
            "2026": {
                "2": "2026-02-04 05:00:00",
                "3": "2026-03-05 23:00:00",
                ...
            }
        }
        """
        with open(solar_terms_json_path, "r", encoding="utf-8") as f:
            self.solar_terms = json.load(f)

    # ----------------------------------------------------------------------
    # 経度補正（任意）
    # ----------------------------------------------------------------------
    def adjust_longitude(self, dt: datetime, city: str | None) -> datetime:
        """
        経度補正を行う。
        city が None の場合は補正しない。
        city が LONGITUDE に存在しない場合も補正しない。
        """
        if city is None:
            return dt

        minute = self.LONGITUDE.get(city.lower(), 0)
        return dt + timedelta(minutes=minute)

    # ----------------------------------------------------------------------
    # 日柱（六十干支）計算
    # ----------------------------------------------------------------------
    def _get_base_days(self, dt: datetime) -> int:
        """
        日柱の六十干支インデックス（0〜59）を求める。

        基準日：
        1900/01/01 = 甲戌日（六十干支インデックス 10）
        """
        base_date = datetime(1900, 1, 1)
        delta_days = (dt.date() - base_date.date()).days
        base_offset = 10  # 甲戌日
        return (delta_days + base_offset) % 60

    # ----------------------------------------------------------------------
    # メイン処理：日時から四柱用インデックスを抽出
    # ----------------------------------------------------------------------
    def evaluate_datetime(self, dt: datetime, city: str | None = None) -> dict:
        """
        指定された日時から四柱推命の各インデックスを抽出する。

        city を指定すると経度補正を行う。
        """
        # 経度補正（任意）
        dt = self.adjust_longitude(dt, city)

        year = dt.year
        month = dt.month

        # ------------------------------------------------------------------
        # 1. 節入り日時の取得
        # ------------------------------------------------------------------
        year_str = str(year)
        month_str = str(month)

        if year_str not in self.solar_terms:
            raise ValueError(f"節入りデータに年 {year_str} がありません")

        if month_str not in self.solar_terms[year_str]:
            raise ValueError(f"節入りデータに {year_str}年 {month_str}月 がありません")

        term_time = datetime.strptime(
            self.solar_terms[year_str][month_str],
            "%Y-%m-%d %H:%M:%S"
        )

        # ------------------------------------------------------------------
        # 2. 節入り前後で「暦上の年・月」を決定
        # ------------------------------------------------------------------
        if dt < term_time:
            calc_month = month - 1
            calc_year = year

            if calc_month == 0:
                calc_month = 12
                calc_year = year - 1
        else:
            calc_month = month
            calc_year = year

        # ------------------------------------------------------------------
        # 3. 年柱の六十干支インデックス
        # ------------------------------------------------------------------
        year_offset = (calc_year - 1984) % 60
        year_kanchi_idx = year_offset if year_offset >= 0 else year_offset + 60

        # ------------------------------------------------------------------
        # 4. 月支インデックス（正統派）
        #
        # 1月=丑(1), 2月=寅(2), ..., 12月=子(0)
        # ------------------------------------------------------------------
        month_branch_idx = (calc_month + 10) % 12

        # ------------------------------------------------------------------
        # 5. 日柱（六十干支インデックス）
        # ------------------------------------------------------------------
        day_kanchi_idx = self._get_base_days(dt)

        # ------------------------------------------------------------------
        # 6. 時支インデックス（透派）
        # ------------------------------------------------------------------
        hour = dt.hour
        if hour == 23:
            hour_branch_idx = 0
        else:
            hour_branch_idx = (hour + 1) // 2

        return {
            "year_kanchi_idx": year_kanchi_idx,
            "month_branch_idx": month_branch_idx,
            "day_kanchi_idx": day_kanchi_idx,
            "hour_branch_idx": hour_branch_idx
        }




