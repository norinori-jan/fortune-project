from datetime import datetime, timedelta, timezone

from scipy.optimize import brentq
from skyfield.api import load


class ShichuCalendar:
    """
    四柱推命暦計算

    ・天文計算による二十四節気
    ・年柱
    ・月柱
    ・日柱
    ・時柱
    """

    LONGITUDE = {
        "tokyo": 18,
        "osaka": 2,
        "nagoya": 8,
        "sendai": 20,
        "sapporo": 25,
        "hiroshima": -6,
        "fukuoka": -18,
        "naha": -29,
    }

    TERM_NAMES = [
        "春分",
        "清明",
        "穀雨",
        "立夏",
        "小満",
        "芒種",
        "夏至",
        "小暑",
        "大暑",
        "立秋",
        "処暑",
        "白露",
        "秋分",
        "寒露",
        "霜降",
        "立冬",
        "小雪",
        "大雪",
        "冬至",
        "小寒",
        "大寒",
        "立春",
        "雨水",
        "啓蟄",
    ]

    def __init__(self, solar_terms_json_path=None):

        self.ts = load.timescale()
        self.eph = load("de440s.bsp")

    # ------------------------------------------------
    # 経度補正
    # ------------------------------------------------
    def adjust_longitude(self, dt, city=None):

        if city is None:
            return dt

        minute = self.LONGITUDE.get(city.lower(), 0)

        return dt + timedelta(minutes=minute)

    # ------------------------------------------------
    # 太陽黄経
    # ------------------------------------------------
    def solar_longitude(self, dt):

        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)

        t = self.ts.from_datetime(dt)

        earth = self.eph["earth"]
        sun = self.eph["sun"]

        astrometric = earth.at(t).observe(sun)
        apparent = astrometric.apparent()

        lon, lat, distance = apparent.ecliptic_latlon()

        return lon.degrees % 360

    # ------------------------------------------------
    # 黄経との差
    # ------------------------------------------------
    def _longitude_diff(self, dt, target):

        lon = self.solar_longitude(dt)

        return (lon - target + 180) % 360 - 180

    # ------------------------------------------------
    # 指定黄経の通過時刻
    # ------------------------------------------------
    def find_term(self, start, target):

        end = start + timedelta(days=3)

        def f(sec):

            dt = start + timedelta(seconds=sec)

            return self._longitude_diff(dt, target)

        sec = brentq(
            f,
            0,
            (end - start).total_seconds(),
        )

        return start + timedelta(seconds=float(sec))

    # ------------------------------------------------
    # 二十四節気
    # ------------------------------------------------
    def get_24_terms(self, year):

        result = {}

        start = datetime(year, 1, 1)

        for i in range(24):

            angle = i * 15

            dt = self.find_term(start, angle)

            result[self.TERM_NAMES[i]] = dt

            start = dt + timedelta(days=10)

        return result

    # ------------------------------------------------
    # 日柱
    # ------------------------------------------------
    def _get_base_days(self, dt):

        base = datetime(1900, 1, 1)

        return ((dt.date() - base.date()).days + 10) % 60

    # ------------------------------------------------
    # メイン
    # ------------------------------------------------
    def evaluate_datetime(self, dt, city=None):

        dt = self.adjust_longitude(dt, city)

        year = dt.year

        terms = self.get_24_terms(year)

        calc_year = year
        calc_month = dt.month

        for term_time in sorted(terms.values()):

            if dt < term_time:

                calc_month -= 1

                if calc_month == 0:
                    calc_month = 12
                    calc_year -= 1

                break

        year_idx = (calc_year - 1984) % 60

        month_branch_idx = (calc_month + 10) % 12

        day_idx = self._get_base_days(dt)

        if dt.hour == 23:
            hour_branch_idx = 0
        else:
            hour_branch_idx = (dt.hour + 1) // 2

        return {
            "year_kanchi_idx": year_idx,
            "month_branch_idx": month_branch_idx,
            "day_kanchi_idx": day_idx,
            "hour_branch_idx": hour_branch_idx,
        }


# ------------------------------------------------
# engine互換
# ------------------------------------------------
def adjust_longitude(dt, longitude):

    if longitude is None:
        return dt

    return dt + timedelta(minutes=longitude * 4)