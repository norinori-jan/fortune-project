from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional, List, Dict

from fortune_core.common.stem import Stem
from fortune_core.common.branch import Branch
from fortune_core.shichu.ten_gods import TenGod
from fortune_core.shichu.twelve_growth import TwelveGrowth


# ------------------------------------------------------------
# 1. 最上段：カレンダー詳細
# ------------------------------------------------------------
@dataclass(frozen=True)
class CalendarDetails:
    solar_term_name: str          # 節入り名（立春、啓蟄など）
    solar_term_time: datetime     # 節入り日時
    shin_sen_days: int            # 深浅（節入りからの日数）
    ritsu_un_years: int           # 立運（何年運か）
    is_reverse: bool              # 順運か逆運か


# ------------------------------------------------------------
# 2. 五行メーター
# ------------------------------------------------------------
@dataclass(frozen=True)
class ElementStrength:
    values: Dict[str, float]      # {"木": 2.5, "火": 1.0, ...}


# ------------------------------------------------------------
# 3. 宅神・基神
# ------------------------------------------------------------
@dataclass(frozen=True)
class HouseGods:
    ha_taku_shin: str             # 破宅神
    taku_shin: str                # 宅神
    ki_shin: str                  # 基神
    ki_seki: str                  # 基石


# ------------------------------------------------------------
# 4. 特殊干支併臨・天地徳合
# ------------------------------------------------------------
@dataclass(frozen=True)
class SpecialCombinations:
    nichigan_heirin_year: Optional[int] = None
    getsugan_heirin_year: Optional[int] = None
    tenchi_tokugo_year: Optional[int] = None


# ------------------------------------------------------------
# 5. 格局・用神
# ------------------------------------------------------------
@dataclass(frozen=True)
class KakukyokuYojin:
    ho_go: Optional[str] = None
    kai_kyoku: Optional[str] = None
    kakukyoku: str
    yojin: str
    kishin: str
    ijin: str
    choko: Optional[str] = None


# ------------------------------------------------------------
# 6. 年運（小運）1年分のマス
# ------------------------------------------------------------
@dataclass(frozen=True)
class NenunCell:
    seireki: int                  # その年の西暦
    age: int                      # その年齢
    kanchi: str                   # 年運の干支（例: "甲子"）
    twelve_growth: TwelveGrowth   # その年の十二運（勢い）


# ------------------------------------------------------------
# 7. 大運（10年）1列分
# ------------------------------------------------------------
@dataclass(frozen=True)
class TaiunRow:
    taiun_seireki: int                    # 大運の開始年
    taiun_kanchi: str                     # 大運の干支
    taiun_ten_god: Optional[TenGod]       # 大運の通変星
    taiun_twelve_growth: TwelveGrowth     # 大運の十二運
    nenun_cells: List[NenunCell]          # その大運に含まれる年運（10年分）


# ------------------------------------------------------------
# 8. 鑑定用紙の四柱縦軸（干・支・蔵・通変・十二運）
# ------------------------------------------------------------
@dataclass(frozen=True)
class PaperPillar:
    stem: Stem
    branch: Branch
    zangkan: str
    stem_ten_god: TenGod
    zangkan_ten_god: TenGod
    twelve_growth: TwelveGrowth


# ------------------------------------------------------------
# 9. 鑑定用紙そのもの（Chart）
# ------------------------------------------------------------
@dataclass(frozen=True)
class Chart:
    """
    透派鑑定用紙（IMG_0775）完全対応・命式オブジェクト
    """

    # 1. 最上段ヘッダー
    birth: datetime
    gender: str
    calendar_details: CalendarDetails

    # 2. 四柱盤面（右上）
    year: PaperPillar
    month: PaperPillar
    day: PaperPillar
    hour: PaperPillar

    # 3. 中段右・中央：看命パラメータ
    kobo: List[str]
    element_strength: ElementStrength
    house_gods: HouseGods
    special_combinations: SpecialCombinations

    # 4. 中央：格局・用神
    analysis: KakukyokuYojin

    # 5. 最下段：大運タイムライン（右→左）
    taiun_timeline: List[TaiunRow] = field(default_factory=list)
