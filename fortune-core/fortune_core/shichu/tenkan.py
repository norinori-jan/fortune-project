# fortune_core/shichu/tenkan.py
from dataclasses import dataclass
from fortune_core.common.stem import Stem
from fortune_core.common.branch import Branch


@dataclass(frozen=True)
class Pillar:
    """一柱（天干と地支のペア）"""
    stem: Stem
    branch: Branch


@dataclass(frozen=True)
class FourPillarsChart:
    """四柱推命の命式（四柱）"""
    year: Pillar
    month: Pillar
    day: Pillar
    hour: Pillar


class ShichuEngine:
    def __init__(self, registry_loader):
        """
        registry_loader は stems.json, branches.json から
        すでに dict[str, Stem], dict[str, Branch] を読み込み済みの想定
        """
        self.stems = registry_loader.get_stems()        # {"甲": Stem(...), ...}
        self.branches = registry_loader.get_branches()  # {"子": Branch(...), ...}

        # インデックス順にソートしたリストを内部で保持
        self.stem_list = sorted(list(self.stems.values()), key=lambda x: x.index)
        self.branch_list = sorted(list(self.branches.values()), key=lambda x: x.index)

    # ----------------------------------------------------------------------
    # 天干・地支のインデックスから Stem / Branch を取得
    # ----------------------------------------------------------------------
    def _get_stem_by_idx(self, idx: int) -> Stem:
        """十干は 10 で循環する"""
        return self.stem_list[idx % 10]

    def _get_branch_by_idx(self, idx: int) -> Branch:
        """十二支は 12 で循環する"""
        return self.branch_list[idx % 12]

    # ----------------------------------------------------------------------
    # 月上起例（年干 → 月干）
    # ----------------------------------------------------------------------
    def calculate_month_stem(self, year_stem_idx: int, month_branch_idx: int) -> Stem:
        """
        【月上起例法】年干から月干を求める（寅月ベース）

        公式：
        月干 = 年干の五行グループ × 2 + 寅月からの差分
        """
        base_stem_idx = (year_stem_idx % 5) * 2 + 2
        diff = (month_branch_idx - 2) % 12
        return self._get_stem_by_idx(base_stem_idx + diff)

    # ----------------------------------------------------------------------
    # 時上起例（日干 → 時干）
    # ----------------------------------------------------------------------
    def calculate_hour_stem(self, day_stem_idx: int, hour_branch_idx: int) -> Stem:
        """
        【時上起例法】日干から時干を求める（子時ベース）

        公式：
        時干 = 日干の五行グループ × 2 + 時支インデックス
        """
        base_stem_idx = (day_stem_idx % 5) * 2
        return self._get_stem_by_idx(base_stem_idx + hour_branch_idx)

    # ----------------------------------------------------------------------
    # 四柱命式の構築
    # ----------------------------------------------------------------------
    def create_chart(self, cal_data: dict) -> FourPillarsChart:
        """
        ShichuCalendar.evaluate_datetime() の返り値(dict)を受け取り、
        完全な四柱命式を作成する
        """

        # -------------------------
        # 年柱（六十干支 → 天干・地支）
        # -------------------------
        y_idx = cal_data["year_kanchi_idx"]
        year_pillar = Pillar(
            stem=self._get_stem_by_idx(y_idx % 10),
            branch=self._get_branch_by_idx(y_idx % 12)
        )

        # -------------------------
        # 月柱（年干 → 月干）
        # -------------------------
        m_b_idx = cal_data["month_branch_idx"]
        month_stem = self.calculate_month_stem(year_pillar.stem.index, m_b_idx)
        month_pillar = Pillar(
            stem=month_stem,
            branch=self._get_branch_by_idx(m_b_idx)
        )

        # -------------------------
        # 日柱（六十干支 → 天干・地支）
        # -------------------------
        d_idx = cal_data["day_kanchi_idx"]
        day_pillar = Pillar(
            stem=self._get_stem_by_idx(d_idx % 10),
            branch=self._get_branch_by_idx(d_idx % 12)
        )

        # -------------------------
        # 時柱（日干 → 時干）
        # -------------------------
        h_b_idx = cal_data["hour_branch_idx"]
        hour_stem = self.calculate_hour_stem(day_pillar.stem.index, h_b_idx)
        hour_pillar = Pillar(
            stem=hour_stem,
            branch=self._get_branch_by_idx(h_b_idx)
        )

        # -------------------------
        # 四柱完成
        # -------------------------
        return FourPillarsChart(
            year=year_pillar,
            month=month_pillar,
            day=day_pillar,
            hour=hour_pillar
        )

