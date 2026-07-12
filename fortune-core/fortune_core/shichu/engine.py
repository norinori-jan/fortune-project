# fortune_core/shichu/engine.py
from datetime import datetime
from typing import List, Optional

from fortune_core.shichu.dataclasses import (
    Chart,
    PaperPillar,
    CalendarDetails,
    ElementStrength,
    HouseGods,
    SpecialCombinations,
    KakukyokuYojin,
    TaiunRow,
    NenunCell,
)

from fortune_core.common.stem import Stem
from fortune_core.common.branch import Branch

from .calendar import ShichuCalendar, adjust_longitude
from .tenkan import ShichuEngine as TenkanEngine
from .zangkan import ZangKanEngine
from .ten_gods import TenGodsEngine
from .twelve_growth import TwelveGrowthEngine
from .gods import GodsEngine


class Engine:

    def __init__(self, registry_loader, solar_terms_json_path: str):
        self.calendar = ShichuCalendar(solar_terms_json_path)
        self.tenkan_engine = TenkanEngine(registry_loader)
        self.zangkan_engine = ZangkanEngine(registry_loader)
        self.ten_gods_engine = TenGodsEngine(registry_loader)
        self.twelve_growth_engine = TwelveGrowthEngine(registry_loader)
        self.gods_engine = GodsEngine(registry_loader)

    # ------------------------------------------------------------
    # 空亡
    # ------------------------------------------------------------
    def _calc_kobo(self, raw_chart) -> List[str]:
        d_stem_idx = raw_chart.day.stem.index
        d_branch_idx = raw_chart.day.branch.index

        shunto_branch_idx = (d_branch_idx - d_stem_idx) % 12

        kobo1_idx = (shunto_branch_idx + 10) % 12
        kobo2_idx = (shunto_branch_idx + 11) % 12

        kobo1_name = self.tenkan_engine.get_branch_by_index(kobo1_idx).name
        kobo2_name = self.tenkan_engine.get_branch_by_index(kobo2_idx).name

        return [kobo1_name, kobo2_name]

    # ------------------------------------------------------------
    # 宅神・基神
    # ------------------------------------------------------------
    def _calc_house_gods(self, raw_chart) -> HouseGods:
        m_branch_idx = raw_chart.month.branch.index

        taku_idx = (m_branch_idx + 5) % 12
        taku_shin = self.tenkan_engine.get_branch_by_index(taku_idx).name

        ha_taku_idx = (taku_idx + 6) % 12
        ha_taku_shin = self.tenkan_engine.get_branch_by_index(ha_taku_idx).name

        ki_shin = raw_chart.day.branch.name
        ki_seki = raw_chart.day.stem.element

        return HouseGods(
            ha_taku_shin=ha_taku_shin,
            taku_shin=taku_shin,
            ki_shin=ki_shin,
            ki_seki=ki_seki,
        )

    # ------------------------------------------------------------
    # 方合・会局
    # ------------------------------------------------------------
    def _detect_combinations(self, branches: List[str]) -> tuple[Optional[str], Optional[str]]:
        branch_set = set(branches)
        ho_go = None
        kai_kyoku = None

        hogo_map = {
            ("寅", "卯", "辰"): "木",
            ("巳", "午", "未"): "火",
            ("申", "酉", "戌"): "金",
            ("亥", "子", "丑"): "水"
        }
        for combo, elem in hogo_map.items():
            if set(combo).issubset(branch_set):
                ho_go = elem
                break

        kaikyoku_map = {
            ("亥", "卯", "未"): "木",
            ("寅", "午", "戌"): "火",
            ("巳", "酉", "丑"): "金",
            ("申", "子", "辰"): "水"
        }
        for combo, elem in kaikyoku_map.items():
            if set(combo).issubset(branch_set):
                kai_kyoku = elem
                break

        return ho_go, kai_kyoku

    # ------------------------------------------------------------
    # 五行量
    # ------------------------------------------------------------
    def _calc_element_strength(self, chart: Chart) -> ElementStrength:
        values = {"木": 0.0, "火": 0.0, "土": 0.0, "金": 0.0, "水": 0.0}

        branches = [
            chart.year.branch.name,
            chart.month.branch.name,
            chart.day.branch.name,
            chart.hour.branch.name,
        ]

        ho_go, kai_kyoku = self._detect_combinations(branches)

        change_elem = ho_go or kai_kyoku
        change_branches = set()

        if change_elem:
            if ho_go:
                change_branches = {"寅", "卯", "辰"} if change_elem == "木" else \
                                  {"巳", "午", "未"} if change_elem == "火" else \
                                  {"申", "酉", "戌"} if change_elem == "金" else \
                                  {"亥", "子", "丑"}
            else:
                change_branches = {"亥", "卯", "未"} if change_elem == "木" else \
                                  {"寅", "午", "戌"} if change_elem == "火" else \
                                  {"巳", "酉", "丑"} if change_elem == "金" else \
                                  {"申", "子", "辰"}

        for pillar in [chart.year, chart.month, chart.day, chart.hour]:
            values[pillar.stem.element] += 1.0

        for pillar in [chart.year, chart.month, chart.day, chart.hour]:
            b_name = pillar.branch.name

            if b_name in change_branches and change_elem:
                values[change_elem] += 1.0
                values[change_elem] += 0.5
            else:
                values[pillar.branch.element] += 1.0

                zang_name = pillar.zangkan
                zang_obj = self.tenkan_engine.registry_loader.get_stems().get(zang_name)
                zang_elem = zang_obj.element if zang_obj else "木"
                values[zang_elem] += 0.5

        return ElementStrength(values=values)

    # ------------------------------------------------------------
    # 格局・用神（高度版：従格判定を含む）
    # ------------------------------------------------------------
    def _detect_jugaku(self, chart: Chart, strength: ElementStrength) -> Optional[str]:
        day_elem = chart.day.stem.element
        values = strength.values

        if values[day_elem] <= 0.5:
            if day_elem == "木" and values["火"] > 2.5:
                return "従財格"
            if day_elem == "水" and values["木"] > 2.5:
                return "従児格"
            if day_elem == "木" and values["金"] > 2.5:
                return "従殺格"
            if values[day_elem] == 0:
                return "従旺格"

        return None

    # ------------------------------------------------------------
    # 調候（寒暖・湿燥）
    # ------------------------------------------------------------
    def _calc_choko(self, chart: Chart) -> Optional[str]:
        month = chart.month.branch.name

        cold = {"亥", "子", "丑"}
        hot = {"巳", "午", "未"}
        wet = {"辰", "丑", "未", "戌"}
        dry = {"寅", "卯", "申", "酉"}

        needs = []

        if month in cold:
            needs.append("火（解寒）")
        if month in hot:
            needs.append("水（解炎）")
        if month in wet:
            needs.append("金（除湿）")
        if month in dry:
            needs.append("木（除燥）")

        return "・".join(needs) if needs else None

    # ------------------------------------------------------------
    # 特殊干支併臨・天地徳合
    # ------------------------------------------------------------
    def _calc_special_combinations(self, chart: Chart) -> SpecialCombinations:
        nichigan = chart.day.stem.name
        getsugan = chart.month.stem.name

        tokugo_set = {"甲子", "乙丑", "庚午", "辛未", "壬申", "癸酉"}

        nichigan_heirin_year = None
        getsugan_heirin_year = None
        tenchi_tokugo_year = None

        for row in chart.taiun_timeline:
            for nen in row.nenun_cells:
                nen_kan = nen.kanchi[0]
                nen_full = nen.kanchi

                if nen_kan == nichigan:
                    nichigan_heirin_year = nen.seireki
                if nen_kan == getsugan:
                    getsugan_heirin_year = nen.seireki
                if nen_full in tokugo_set:
                    tenchi_tokugo_year = nen.seireki

        return SpecialCombinations(
            nichigan_heirin_year=nichigan_heirin_year,
            getsugan_heirin_year=getsugan_heirin_year,
            tenchi_tokugo_year=tenchi_tokugo_year,
        )

    # ------------------------------------------------------------
    # 大運干支（透派式）
    # ------------------------------------------------------------
    def _taiun_kanchi(self, raw_chart, step: int, is_reverse: bool, gender: str) -> str:
        kanchi_list = self._get_kanchi_list()

        m_stem_idx = raw_chart.month.stem.index
        m_branch_idx = raw_chart.month.branch.index

        base_idx = None
        for i in range(60):
            if i % 10 == m_stem_idx and i % 12 == m_branch_idx:
                base_idx = i
                break

        if base_idx is None:
            base_idx = 0

        reverse = is_reverse
        if gender == "男":
            reverse = not reverse

        idx = (base_idx - step) % 60 if reverse else (base_idx + step) % 60

        return kanchi_list[idx]
    # ------------------------------------------------------------
    # 大運＋年運（完全版）
    # ------------------------------------------------------------
    def _build_taiun_timeline(self, raw_chart, cal, adjusted_birth: datetime) -> List[TaiunRow]:
        day_stem = raw_chart.day.stem
        base_year = adjusted_birth.year
        start_age = cal["ritsu_un_years"]
        is_reverse = cal["is_reverse"]

        timeline: List[TaiunRow] = []

        for i in range(8):  # 80年分の大運
            taiun_age = start_age + i * 10
            taiun_start_year = base_year + taiun_age

            # ★ 大運干支（透派式完全版）
            taiun_kanchi = self._taiun_kanchi(
                raw_chart,
                step=i,
                is_reverse=is_reverse,
                gender=raw_chart.gender
            )

            # 大運の支
            taiun_branch_name = taiun_kanchi[1]
            taiun_branch = self.tenkan_engine.registry_loader.get_branches()[taiun_branch_name]

            # 大運十二運
            taiun_twelve = self.twelve_growth_engine.get_growth(day_stem, taiun_branch)

            # 大運通変星
            taiun_stem_name = taiun_kanchi[0]
            taiun_stem = self.tenkan_engine.registry_loader.get_stems()[taiun_stem_name]
            taiun_ten_god = self.ten_gods_engine.get_ten_god(day_stem, taiun_stem)

            # 年運10年分
            nenun_cells: List[NenunCell] = []
            for j in range(10):
                age = taiun_age + j
                year = base_year + age

                # ★ 年運干支（透派式）
                nen_kanchi = self._nenun_kanchi(year)

                nen_branch_name = nen_kanchi[1]
                nen_branch = self.tenkan_engine.registry_loader.get_branches()[nen_branch_name]
                nen_twelve = self.twelve_growth_engine.get_growth(day_stem, nen_branch)

                nenun_cells.append(
                    NenunCell(
                        seireki=year,
                        age=age,
                        kanchi=nen_kanchi,
                        twelve_growth=nen_twelve,
                    )
                )

            timeline.append(
                TaiunRow(
                    taiun_seireki=taiun_start_year,
                    taiun_kanchi=taiun_kanchi,
                    taiun_ten_god=taiun_ten_god,
                    taiun_twelve_growth=taiun_twelve,
                    nenun_cells=nenun_cells,
                )
            )

        return timeline

    # ------------------------------------------------------------
    # メイン：鑑定用紙 Chart を返す（完全版）
    # ------------------------------------------------------------
    def generate(self, birth: datetime, gender: str, longitude=None) -> Chart:
        adjusted_birth = adjust_longitude(birth, longitude)
        cal = self.calendar.evaluate_datetime(adjusted_birth)

        calendar_details = CalendarDetails(
            solar_term_name=cal["solar_term_name"],
            solar_term_time=cal["solar_term_time"],
            shin_sen_days=cal["shin_sen_days"],
            ritsu_un_years=cal["ritsu_un_years"],
            is_reverse=cal["is_reverse"],
        )

        raw_chart = self.tenkan_engine.create_chart(cal)
        raw_chart.gender = gender  # ★ 大運逆運判定に必要

        # 蔵干
        z_year = self.zangkan_engine.get_zangkan(raw_chart.year.branch)
        z_month = self.zangkan_engine.get_zangkan(raw_chart.month.branch)
        z_day = self.zangkan_engine.get_zangkan(raw_chart.day.branch)
        z_hour = self.zangkan_engine.get_zangkan(raw_chart.hour.branch)

        # 四柱の Pillar を作成
        def build_pillar(stem: Stem, branch: Branch, zang: str) -> PaperPillar:
            stem_tg = self.ten_gods_engine.get_ten_god(raw_chart.day.stem, stem)
            zang_tg = self.ten_gods_engine.get_ten_god(raw_chart.day.stem, branch)
            twelve = self.twelve_growth_engine.get_growth(raw_chart.day.stem, branch)
            return PaperPillar(
                stem=stem,
                branch=branch,
                zangkan=zang,
                stem_ten_god=stem_tg,
                zangkan_ten_god=zang_tg,
                twelve_growth=twelve,
            )

        year_pillar = build_pillar(raw_chart.year.stem, raw_chart.year.branch, z_year)
        month_pillar = build_pillar(raw_chart.month.stem, raw_chart.month.branch, z_month)
        day_pillar = build_pillar(raw_chart.day.stem, raw_chart.day.branch, z_day)
        hour_pillar = build_pillar(raw_chart.hour.stem, raw_chart.hour.branch, z_hour)

        # 仮 Chart（五行計算などに使う）
        tmp_chart = Chart(
            birth=adjusted_birth,
            gender=gender,
            calendar_details=calendar_details,
            year=year_pillar,
            month=month_pillar,
            day=day_pillar,
            hour=hour_pillar,
            kobo=[],
            element_strength=ElementStrength(values={"木": 0, "火": 0, "土": 0, "金": 0, "水": 0}),
            house_gods=HouseGods("", "", "", ""),
            special_combinations=SpecialCombinations(),
            analysis=KakukyokuYojin("", "", "", "", None, None, None),
            taiun_timeline=[],
        )

        # 大運タイムライン
        taiun_timeline = self._build_taiun_timeline(raw_chart, cal, adjusted_birth)
        tmp_chart.taiun_timeline = taiun_timeline

        # 各種計算
        kobo = self._calc_kobo(raw_chart)
        house_gods = self._calc_house_gods(raw_chart)
        element_strength = self._calc_element_strength(tmp_chart)
        special_combinations = self._calc_special_combinations(tmp_chart)

        # 格局・用神（従格判定含む）
        jugaku = self._detect_jugaku(tmp_chart, element_strength)
        analysis = self._calc_analysis(tmp_chart)
        if jugaku:
            analysis.kakukyoku = jugaku

        # 調候（寒暖・湿燥）
        analysis.choko = self._calc_choko(tmp_chart)

        # 最終 Chart を返す
        return Chart(
            birth=adjusted_birth,
            gender=gender,
            calendar_details=calendar_details,
            year=year_pillar,
            month=month_pillar,
            day=day_pillar,
            hour=hour_pillar,
            kobo=kobo,
            element_strength=element_strength,
            house_gods=house_gods,
            special_combinations=special_combinations,
            analysis=analysis,
            taiun_timeline=taiun_timeline,
        )
    # ------------------------------------------------------------
    # 流年（西暦 → NenunCell）
    # ------------------------------------------------------------
    def get_nenun(self, chart: Chart, target_year: int) -> Optional[NenunCell]:
        for row in chart.taiun_timeline:
            for nen in row.nenun_cells:
                if nen.seireki == target_year:
                    return nen
        return None

    # ------------------------------------------------------------
    # 流年（詳細版：通変星付き）
    # ------------------------------------------------------------
    def get_nenun_detail(self, chart: Chart, target_year: int):
        nen = self.get_nenun(chart, target_year)
        if nen is None:
            return None

        day_stem = chart.day.stem
        nen_stem = self.tenkan_engine.registry_loader.get_stems()[nen.kanchi[0]]
        nen_ten_god = self.ten_gods_engine.get_ten_god(day_stem, nen_stem)

        return {
            "seireki": nen.seireki,
            "age": nen.age,
            "kanchi": nen.kanchi,
            "twelve_growth": nen.twelve_growth,
            "ten_god": nen_ten_god,
        }

    # ------------------------------------------------------------
    # 現在の大運（年齢から自動判定）
    # ------------------------------------------------------------
    def get_current_taiun(self, chart: Chart, today: datetime) -> Optional[TaiunRow]:
        age = today.year - chart.birth.year
        for row in chart.taiun_timeline:
            start_age = row.taiun_seireki - chart.birth.year
            end_age = start_age + 10
            if start_age <= age < end_age:
                return row
        return None

    # ------------------------------------------------------------
    # 流月（年運＋月干支＋十二運）
    # ------------------------------------------------------------
    def get_ryugetsu(self, chart: Chart, target_year: int, target_month: int):
        nen = self.get_nenun(chart, target_year)
        if nen is None:
            return None

        dt = datetime(target_year, target_month, 1)
        cal = self.calendar.evaluate_datetime(dt)
        month_stem = self.tenkan_engine.registry_loader.get_stems()[cal["month_stem"]]
        month_branch = self.tenkan_engine.registry_loader.get_branches()[cal["month_branch"]]

        twelve = self.twelve_growth_engine.get_growth(chart.day.stem, month_branch)
        ten_god = self.ten_gods_engine.get_ten_god(chart.day.stem, month_stem)

        return {
            "year": target_year,
            "month": target_month,
            "nenun": nen,
            "month_kanchi": month_stem.name + month_branch.name,
            "twelve_growth": twelve,
            "ten_god": ten_god,
        }

    # ------------------------------------------------------------
    # 流日（対象日 → 日干支＋十二運＋通変星）
    # ------------------------------------------------------------
    def get_ryunichi(self, chart: Chart, target_date: datetime):
        cal = self.calendar.evaluate_datetime(target_date)

        day_stem = self.tenkan_engine.registry_loader.get_stems()[cal["day_stem"]]
        day_branch = self.tenkan_engine.registry_loader.get_branches()[cal["day_branch"]]

        twelve = self.twelve_growth_engine.get_growth(chart.day.stem, day_branch)
        ten_god = self.ten_gods_engine.get_ten_god(chart.day.stem, day_stem)

        return {
            "date": target_date,
            "kanchi": day_stem.name + day_branch.name,
            "twelve_growth": twelve,
            "ten_god": ten_god,
        }
class AIExplain:
    """
    命式の各要素を自然言語で説明する層。
    Chart を入力にして文章を返す。
    """

    def explain_kakukyoku(self, chart: Chart) -> str:
        kk = chart.analysis.kakukyoku
        if not kk:
            return "この命式には特別な格局は見られません。日主の強弱と五行の配置に基づく通常の判断となります。"

        return f"この命式は「{kk}」に該当します。従格は日主の力が極端に弱く、他の五行が強く支配することで成立します。"

    def explain_yojin(self, chart: Chart) -> str:
        yj = chart.analysis.yojin
        if not yj:
            return "用神は特定されていません。五行の偏りが小さく、全体のバランスを重視する命式です。"

        return f"この命式の用神は「{yj}」です。五行の偏りを補い、命式全体の調和を保つ重要な要素です。"

    def explain_choko(self, chart: Chart) -> str:
        ck = chart.analysis.choko
        if not ck:
            return "調候上の大きな偏りはありません。季節の気に対して特別な補正は不要です。"

        return f"調候では「{ck}」が必要とされます。これは季節の寒暖・湿燥に応じて五行の補正を行うためです。"

    def explain_special(self, chart: Chart) -> str:
        sp = chart.special_combinations
        msgs = []

        if sp.nichigan_heirin_year:
            msgs.append(f"日干併臨が {sp.nichigan_heirin_year} 年に巡ります。日主の象意が強く現れやすい年です。")

        if sp.getsugan_heirin_year:
            msgs.append(f"月干併臨が {sp.getsugan_heirin_year} 年に巡ります。月柱の象意が強く現れやすい年です。")

        if sp.tenchi_tokugo_year:
            msgs.append(f"天地徳合が {sp.tenchi_tokugo_year} 年に成立します。非常に吉祥で、調和と幸運が強まる年です。")

        if not msgs:
            return "特殊干支の併臨や天地徳合は見られません。"

        return " ".join(msgs)

    def explain_element_balance(self, chart: Chart) -> str:
        vals = chart.element_strength.values
        msg = "五行のバランスは以下の通りです：\n"
        for k, v in vals.items():
            msg += f"・{k}: {v}\n"

        return msg + "この五行の偏りをもとに、用神や調候が判断されます。"

    def explain_all(self, chart: Chart) -> str:
        """
        全体の解説をまとめて返す。
        """
        parts = [
            self.explain_kakukyoku(chart),
            self.explain_yojin(chart),
            self.explain_choko(chart),
            self.explain_special(chart),
            self.explain_element_balance(chart),
        ]
        return "\n\n".join(parts)
class AIReading:
    """
    命式＋運勢を総合して鑑定文を生成する層。
    Chart と運勢 API を使って文章を返す。
    """

    def summarize_meishiki(self, chart: Chart) -> str:
        kk = chart.analysis.kakukyoku or "通常格"
        yj = chart.analysis.yojin or "特定なし"
        choko = chart.analysis.choko or "特別な調候補正なし"

        return (
            f"【命式の性質】\n"
            f"・格局：{kk}\n"
            f"・用神：{yj}\n"
            f"・調候：{choko}\n"
        )

    def summarize_taiun(self, chart: Chart, taiun: TaiunRow) -> str:
        tg = taiun.taiun_ten_god.name
        tg12 = taiun.taiun_twelve_growth.name
        kanchi = taiun.taiun_kanchi

        return (
            f"【大運のテーマ】\n"
            f"・大運干支：{kanchi}\n"
            f"・通変星：{tg}\n"
            f"・十二運：{tg12}\n"
            f"この10年間は、上記の象意が強く働く時期となります。\n"
        )

    def summarize_nenun(self, nen: NenunCell, chart: Chart) -> str:
        tg = chart.ten_gods_engine.get_ten_god(chart.day.stem,
                                               chart.tenkan_engine.registry_loader.get_stems()[nen.kanchi[0]])
        tg12 = nen.twelve_growth.name

        return (
            f"【流年のテーマ（{nen.seireki}年）】\n"
            f"・年干支：{nen.kanchi}\n"
            f"・通変星：{tg.name}\n"
            f"・十二運：{tg12}\n"
        )

    def summarize_month(self, ryugetsu: dict) -> str:
        return (
            f"【流月のテーマ（{ryugetsu['year']}年{ryugetsu['month']}月）】\n"
            f"・月干支：{ryugetsu['month_kanchi']}\n"
            f"・通変星：{ryugetsu['ten_god'].name}\n"
            f"・十二運：{ryugetsu['twelve_growth'].name}\n"
        )

    def summarize_day(self, ryunichi: dict) -> str:
        return (
            f"【流日のテーマ（{ryunichi['date'].strftime('%Y-%m-%d')}）】\n"
            f"・日干支：{ryunichi['kanchi']}\n"
            f"・通変星：{ryunichi['ten_god'].name}\n"
            f"・十二運：{ryunichi['twelve_growth'].name}\n"
        )

    def full_reading(self, chart: Chart, engine: Engine, target_year: int, target_month: int, target_date: datetime) -> str:
        """
        命式＋大運＋流年＋流月＋流日をまとめた総合鑑定文を返す。
        """

        # 命式
        meishiki = self.summarize_meishiki(chart)

        # 大運
        taiun = engine.get_current_taiun(chart, target_date)
        taiun_text = self.summarize_taiun(chart, taiun) if taiun else "大運情報なし\n"

        # 流年
        nen = engine.get_nenun(chart, target_year)
        nen_text = self.summarize_nenun(nen, chart) if nen else "流年情報なし\n"

        # 流月
        ryugetsu = engine.get_ryugetsu(chart, target_year, target_month)
        ryugetsu_text = self.summarize_month(ryugetsu) if ryugetsu else "流月情報なし\n"

        # 流日
        ryunichi = engine.get_ryunichi(chart, target_date)
        ryunichi_text = self.summarize_day(ryunichi) if ryunichi else "流日情報なし\n"

        # 総合まとめ
        return (
            "==============================\n"
            "　　　【総合鑑定】\n"
            "==============================\n\n"
            + meishiki + "\n"
            + taiun_text + "\n"
            + nen_text + "\n"
            + ryugetsu_text + "\n"
            + ryunichi_text + "\n"
            + "以上の象意を総合すると、今年は命式の性質と大運・流年の影響が重なり、"
              "特に重要なテーマが浮かび上がる一年となります。\n"
        )
class AIQA:
    """
    ユーザーの質問に応じて、命式＋運勢から回答を生成する層。
    Engine と Chart を使って回答する。
    """

    def __init__(self, engine: Engine):
        self.engine = engine

    # ------------------------------------------------------------
    # 質問の分類
    # ------------------------------------------------------------
    def classify(self, question: str) -> str:
        q = question

        if "仕事" in q or "キャリア" in q:
            return "work"
        if "恋愛" in q or "結婚" in q:
            return "love"
        if "健康" in q:
            return "health"
        if "金運" in q or "財" in q:
            return "money"
        if "今年" in q or "流年" in q:
            return "nenun"
        if "大運" in q:
            return "taiun"

        return "general"

    # ------------------------------------------------------------
    # 流年の象意から回答
    # ------------------------------------------------------------
    def answer_nenun(self, chart: Chart, year: int) -> str:
        nen = self.engine.get_nenun(chart, year)
        if nen is None:
            return f"{year}年の流年情報は取得できませんでした。"

        tg = self.engine.ten_gods_engine.get_ten_god(
            chart.day.stem,
            self.engine.tenkan_engine.registry_loader.get_stems()[nen.kanchi[0]]
        )

        return (
            f"{year}年の流年は「{nen.kanchi}」。\n"
            f"通変星は『{tg.name}』、十二運は『{nen.twelve_growth.name}』です。\n"
            f"この年は、これらの象意が強く働く一年になります。"
        )

    # ------------------------------------------------------------
    # 大運の象意から回答
    # ------------------------------------------------------------
    def answer_taiun(self, chart: Chart, today: datetime) -> str:
        taiun = self.engine.get_current_taiun(chart, today)
        if taiun is None:
            return "現在の大運情報が取得できませんでした。"

        return (
            f"現在の大運は「{taiun.taiun_kanchi}」。\n"
            f"通変星は『{taiun.taiun_ten_god.name}』、十二運は『{taiun.taiun_twelve_growth.name}』です。\n"
            f"この10年間は、これらの象意が人生のテーマとして強く現れます。"
        )

    # ------------------------------------------------------------
    # 分野別回答（仕事・恋愛・健康・金運）
    # ------------------------------------------------------------
    def answer_field(self, field: str, chart: Chart, year: int) -> str:
        nen = self.engine.get_nenun(chart, year)
        if nen is None:
            return f"{year}年の流年情報が取得できませんでした。"

        tg = self.engine.ten_gods_engine.get_ten_god(
            chart.day.stem,
            self.engine.tenkan_engine.registry_loader.get_stems()[nen.kanchi[0]]
        )

        base = f"{year}年の通変星は『{tg.name}』、十二運は『{nen.twelve_growth.name}』です。\n"

        if field == "work":
            return base + "仕事運では、通変星の象意がキャリア・評価・成果に影響します。"
        if field == "love":
            return base + "恋愛運では、通変星の象意が人間関係・縁・感情面に影響します。"
        if field == "health":
            return base + "健康運では、十二運の勢いが体調の上下に影響します。"
        if field == "money":
            return base + "金運では、通変星の象意が収入・支出・財の動きに影響します。"

        return base + "総合的に、これらの象意が一年のテーマとなります。"

    # ------------------------------------------------------------
    # メイン：質問に答える
    # ------------------------------------------------------------
    def answer(self, chart: Chart, question: str, today: datetime) -> str:
        field = self.classify(question)

        year = today.year

        if field == "nenun":
            return self.answer_nenun(chart, year)

        if field == "taiun":
            return self.answer_taiun(chart, today)

        if field in ["work", "love", "health", "money"]:
            return self.answer_field(field, chart, year)

        return "命式と運勢に基づく一般的な回答が可能です。もう少し具体的に質問してください。"

