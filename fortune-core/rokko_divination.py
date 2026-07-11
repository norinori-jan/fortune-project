"""
六爻占術判定エンジン - 完�E実裁E
月破・日破・暗動・用神�E析を含む
"""

from __future__ import annotations
from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Optional
import unittest


# ─────────────────────────────────────────────
# 基本列挙垁E
# ─────────────────────────────────────────────

class GoXing(Enum):
    """五衁E""
    WOOD  = "木"
    FIRE  = "火"
    EARTH = "圁E
    METAL = "釁E
    WATER = "水"


class DiZhi(Enum):
    """十二地支�E�E=孁E、E11=亥�E�E""
    ZI  = 0   # 孁E水
    CHOU = 1  # 丁E圁E
    YIN  = 2  # 寁E木
    MAO  = 3  # 卯 木
    CHEN = 4  # 辰 圁E
    SI   = 5  # 巳 火
    WU   = 6  # 十E火
    WEI  = 7  # 未 圁E
    SHEN = 8  # 申 釁E
    YOU  = 9  # 酁E釁E
    XU   = 10 # 戁E圁E
    HAI  = 11 # 亥 水


class LiuQin(Enum):
    """六親"""
    XIONG_DI  = "允E��爻"   # 比和
    ZI_SUN    = "子孫爻"   # 我生
    QI_CAI    = "妻財爻"   # 我剋
    GUAN_GUI  = "官鬼爻"   # 剋�E
    FU_MU     = "父母爻"   # 生�E


class YaoState(Enum):
    """爻の動静"""
    STATIC  = "静爻"
    DYNAMIC = "動爻"


class WangShuai(Enum):
    """旺衰状慁E""
    WANG   = "旺"    # 最強
    XIANG  = "相"    # 次旺
    XIU    = "企E    # めE��弱
    QI     = "囁E    # 弱
    SI     = "死"    # 最弱


# ─────────────────────────────────────────────
# 五行対応テーブル
# ─────────────────────────────────────────────

DIZHI_WUXING: dict[DiZhi, GoXing] = {
    DiZhi.ZI:   GoXing.WATER,
    DiZhi.CHOU: GoXing.EARTH,
    DiZhi.YIN:  GoXing.WOOD,
    DiZhi.MAO:  GoXing.WOOD,
    DiZhi.CHEN: GoXing.EARTH,
    DiZhi.SI:   GoXing.FIRE,
    DiZhi.WU:   GoXing.FIRE,
    DiZhi.WEI:  GoXing.EARTH,
    DiZhi.SHEN: GoXing.METAL,
    DiZhi.YOU:  GoXing.METAL,
    DiZhi.XU:   GoXing.EARTH,
    DiZhi.HAI:  GoXing.WATER,
}

# 相沖�Eア�E�差ぁE�E�E
CHONG_PAIRS: list[tuple[DiZhi, DiZhi]] = [
    (DiZhi.ZI,  DiZhi.WU),
    (DiZhi.CHOU, DiZhi.WEI),
    (DiZhi.YIN,  DiZhi.SHEN),
    (DiZhi.MAO,  DiZhi.YOU),
    (DiZhi.CHEN, DiZhi.XU),
    (DiZhi.SI,   DiZhi.HAI),
]

# 季節ごとの旺相休囚死�E�月建の五衁EↁE吁E��行�E状態！E
# キー: 月建五衁E 値: {爻五衁E WangShuai}
MONTHLY_WANGSHUAI: dict[GoXing, dict[GoXing, WangShuai]] = {
    GoXing.WOOD: {
        GoXing.WOOD:  WangShuai.WANG,
        GoXing.FIRE:  WangShuai.XIANG,
        GoXing.WATER: WangShuai.XIU,
        GoXing.METAL: WangShuai.QI,
        GoXing.EARTH: WangShuai.SI,
    },
    GoXing.FIRE: {
        GoXing.FIRE:  WangShuai.WANG,
        GoXing.EARTH: WangShuai.XIANG,
        GoXing.WOOD:  WangShuai.XIU,
        GoXing.WATER: WangShuai.QI,
        GoXing.METAL: WangShuai.SI,
    },
    GoXing.EARTH: {
        GoXing.EARTH: WangShuai.WANG,
        GoXing.METAL: WangShuai.XIANG,
        GoXing.FIRE:  WangShuai.XIU,
        GoXing.WOOD:  WangShuai.QI,
        GoXing.WATER: WangShuai.SI,
    },
    GoXing.METAL: {
        GoXing.METAL: WangShuai.WANG,
        GoXing.WATER: WangShuai.XIANG,
        GoXing.EARTH: WangShuai.XIU,
        GoXing.FIRE:  WangShuai.QI,
        GoXing.WOOD:  WangShuai.SI,
    },
    GoXing.WATER: {
        GoXing.WATER: WangShuai.WANG,
        GoXing.WOOD:  WangShuai.XIANG,
        GoXing.METAL: WangShuai.XIU,
        GoXing.EARTH: WangShuai.QI,
        GoXing.FIRE:  WangShuai.SI,
    },
}


# ─────────────────────────────────────────────
# ユーチE��リチE��関数
# ─────────────────────────────────────────────

def is_chong(a: DiZhi, b: DiZhi) -> bool:
    """2つの地支が相沖かどぁE��"""
    return (a, b) in CHONG_PAIRS or (b, a) in CHONG_PAIRS


def wuxing_of(dz: DiZhi) -> GoXing:
    return DIZHI_WUXING[dz]


def wang_shuai(yao_wuxing: GoXing, yuejian: DiZhi) -> WangShuai:
    """爻五行と月建から旺衰を計箁E""
    month_wx = wuxing_of(yuejian)
    return MONTHLY_WANGSHUAI[month_wx][yao_wuxing]


def is_wang_xiang(ws: WangShuai) -> bool:
    return ws in (WangShuai.WANG, WangShuai.XIANG)


# ─────────────────────────────────────────────
# チE�Eタ構造
# ─────────────────────────────────────────────

@dataclass
class Yao:
    """一爻の完�E惁E��"""
    position: int           # 1、E�E��E爻=1, 上爻=6�E�E
    liu_qin:  LiuQin
    di_zhi:   DiZhi
    state:    YaoState      # 静爻 or 動爻
    bian_zhi: Optional[DiZhi] = None   # 変爻�E�動爻のみ�E�E

    @property
    def wuxing(self) -> GoXing:
        return wuxing_of(self.di_zhi)


@dataclass
class DivinationContext:
    """占断の斁E��"""
    yao_list:  list[Yao]    # 6爻�E�Eosition=1、E�E�E
    yuejian:   DiZhi        # 月建
    rizhen:    DiZhi        # 日辰
    shi_yao:   int          # 世爻の位置�E�E、E�E�E
    ying_yao:  int          # 応爻の位置�E�E、E�E�E


@dataclass
class YaoAnalysis:
    """一爻の刁E��結果"""
    yao:         Yao
    wang_shuai:  WangShuai
    yue_po:      bool        # 月破
    ri_po:       bool        # 日破
    an_dong:     bool        # 暗動
    ri_sheng:    bool        # 日辰に生じられめE
    ri_ke:       bool        # 日辰に剋される
    effective_strength: int  # 実効力！E2、E4�E�E

    @property
    def is_po(self) -> bool:
        return self.yue_po or self.ri_po

    @property
    def is_active(self) -> bool:
        """実質皁E��「動ぁE��ぁE��」か�E�動爻 or 暗動�E�E""
        return self.yao.state == YaoState.DYNAMIC or self.an_dong

    def summary(self) -> str:
        flags = []
        if self.yue_po:   flags.append("月破")
        if self.ri_po:    flags.append("日破")
        if self.an_dong:  flags.append("暗動")
        if self.ri_sheng: flags.append("日甁E)
        if self.ri_ke:    flags.append("日剁E)
        flag_str = "・".join(flags) if flags else "なぁE
        return (
            f"[{self.yao.position}爻 {self.yao.liu_qin.value} {self.yao.di_zhi.name} "
            f"{self.yao.state.value}] "
            f"旺衰={self.wang_shuai.value} 特殁E{flag_str} "
            f"実効劁E{self.effective_strength:+d}"
        )


@dataclass
class DivinationResult:
    """占断結果全佁E""
    context:          DivinationContext
    yao_analyses:     list[YaoAnalysis]
    yong_shen_pos:    int          # 用神�E位置
    fu_yong_shen_pos: Optional[int]# 副用神�E位置
    verdict:          str
    detail:           str
    score:            int          # -10、E10の総合スコア


# ─────────────────────────────────────────────
# EnergyAnalyzer
# ─────────────────────────────────────────────

class EnergyAnalyzer:
    """
    吁E��のエネルギー状態を刁E��する、E

    月破�E�月建と相沁EↁEエネルギー消滁E��破砕フラグ ON�E�E
    日破�E�日辰と相沁EↁEエネルギー消滁E��破砕フラグ ON�E�E
    暗動�E�静爻 かつ 旺相 かつ 日辰と相沁EↁE暗動フラグ ON
          ※暗動は日破と同時成立しなぁE��暗動が優先される条件�E�E
             実裁E���E「旺相静爻が沖される」場合�Eみ暗動とし、E
             「休囚死の静爻が沖される」場合�E日破とする、E
    """

    @staticmethod
    def analyze(yao: Yao, yuejian: DiZhi, rizhen: DiZhi) -> YaoAnalysis:
        yao_wx     = yao.wuxing
        month_wx   = wuxing_of(yuejian)
        rizhen_wx  = wuxing_of(rizhen)
        ws         = wang_shuai(yao_wx, yuejian)

        chong_month = is_chong(yao.di_zhi, yuejian)
        chong_ri    = is_chong(yao.di_zhi, rizhen)
        is_static   = yao.state == YaoState.STATIC

        # 月破・日破・暗動の判宁E
        yue_po  = False
        ri_po   = False
        an_dong = False

        if chong_month:
            yue_po = True   # 月建と沁EↁE月破�E�常に�E�E

        if chong_ri:
            if is_static and is_wang_xiang(ws):
                # 旺相の静爻が日辰に沖される ↁE暗動
                an_dong = True
            else:
                # 休囚死の静爻、また�E動爻が日辰に沖される ↁE日破
                ri_po = True

        # 日生�E日剁E
        ri_sheng = EnergyAnalyzer._sheng(rizhen_wx, yao_wx)
        ri_ke    = EnergyAnalyzer._ke(rizhen_wx, yao_wx)

        # 実効力計箁E
        strength = EnergyAnalyzer._calc_strength(
            ws, yue_po, ri_po, an_dong, ri_sheng, ri_ke,
            yao.state == YaoState.DYNAMIC
        )

        return YaoAnalysis(
            yao=yao,
            wang_shuai=ws,
            yue_po=yue_po,
            ri_po=ri_po,
            an_dong=an_dong,
            ri_sheng=ri_sheng,
            ri_ke=ri_ke,
            effective_strength=strength,
        )

    # 五行生剁E
    @staticmethod
    def _sheng(src: GoXing, dst: GoXing) -> bool:
        """src ぁEdst を生ずる"""
        table = {
            GoXing.WOOD:  GoXing.FIRE,
            GoXing.FIRE:  GoXing.EARTH,
            GoXing.EARTH: GoXing.METAL,
            GoXing.METAL: GoXing.WATER,
            GoXing.WATER: GoXing.WOOD,
        }
        return table[src] == dst

    @staticmethod
    def _ke(src: GoXing, dst: GoXing) -> bool:
        """src ぁEdst を剋ぁE""
        table = {
            GoXing.WOOD:  GoXing.EARTH,
            GoXing.EARTH: GoXing.WATER,
            GoXing.WATER: GoXing.FIRE,
            GoXing.FIRE:  GoXing.METAL,
            GoXing.METAL: GoXing.WOOD,
        }
        return table[src] == dst

    @staticmethod
    def _calc_strength(
        ws: WangShuai,
        yue_po: bool,
        ri_po: bool,
        an_dong: bool,
        ri_sheng: bool,
        ri_ke: bool,
        is_dynamic: bool,
    ) -> int:
        # 基礎点
        base = {
            WangShuai.WANG:  4,
            WangShuai.XIANG: 3,
            WangShuai.XIU:   1,
            WangShuai.QI:    0,
            WangShuai.SI:   -1,
        }[ws]

        # 破砕�E力を消滁E��せる
        if yue_po or ri_po:
            return -2

        # 暗動は動爻扱ぁE��+1
        if an_dong:
            base += 1

        # 動爻はさらに+1
        if is_dynamic:
            base += 1

        # 日生�E日剁E
        if ri_sheng:
            base += 1
        if ri_ke:
            base -= 1

        return max(-2, min(base, 6))


# ─────────────────────────────────────────────
# TargetGodMapper
# ─────────────────────────────────────────────

class QuestionType(Enum):
    CAREER       = "仕事�E昁E��"
    WEALTH       = "財運�E投賁E
    MARRIAGE     = "婚姻・恋�E"
    HEALTH       = "健康・痁E��E
    LAWSUIT      = "訴訟�E裁判"
    TRAVEL       = "旁E���E移勁E
    LOST_OBJECT  = "失物・紛失"
    EXAM         = "試験�E賁E��"


@dataclass
class GodMapping:
    yong_shen:     LiuQin
    fu_yong_shen:  Optional[LiuQin]
    description:   str


QUESTION_GOD_MAP: dict[QuestionType, GodMapping] = {
    QuestionType.CAREER: GodMapping(
        yong_shen=LiuQin.GUAN_GUI,
        fu_yong_shen=LiuQin.FU_MU,
        description="仕事�E官鬼爻が用神。父母爻が副用神（文書・印綬�E�、E,
    ),
    QuestionType.WEALTH: GodMapping(
        yong_shen=LiuQin.QI_CAI,
        fu_yong_shen=LiuQin.ZI_SUN,
        description="財運�E妻財爻が用神。子孫爻が副用神（財を生ずる�E�、E,
    ),
    QuestionType.MARRIAGE: GodMapping(
        yong_shen=LiuQin.GUAN_GUI,
        fu_yong_shen=LiuQin.QI_CAI,
        description="婚姻�E�女性占�E��E官鬼爻が用神。妻財爻が副用神、E,
    ),
    QuestionType.HEALTH: GodMapping(
        yong_shen=LiuQin.ZI_SUN,
        fu_yong_shen=None,
        description="健康は子孫爻が用神（官鬼�E�病邪を剋す）、E,
    ),
    QuestionType.LAWSUIT: GodMapping(
        yong_shen=LiuQin.GUAN_GUI,
        fu_yong_shen=LiuQin.XIONG_DI,
        description="訴訟�E官鬼爻が用神。�E弟爻は財を散らし不吉、E,
    ),
    QuestionType.TRAVEL: GodMapping(
        yong_shen=LiuQin.ZI_SUN,
        fu_yong_shen=LiuQin.QI_CAI,
        description="旁E���E子孫爻が用神（頁E��・安�Eを示す）、E,
    ),
    QuestionType.LOST_OBJECT: GodMapping(
        yong_shen=LiuQin.QI_CAI,
        fu_yong_shen=LiuQin.ZI_SUN,
        description="失物は妻財爻が用神（財物を表す）、E,
    ),
    QuestionType.EXAM: GodMapping(
        yong_shen=LiuQin.FU_MU,
        fu_yong_shen=LiuQin.GUAN_GUI,
        description="試験�E父母爻が用神（文書・知識）、E,
    ),
}


class TargetGodMapper:
    """質問タイプから用神�E副用神を決定すめE""

    @staticmethod
    def get_mapping(qtype: QuestionType) -> GodMapping:
        return QUESTION_GOD_MAP[qtype]

    @staticmethod
    def find_yong_shen(ctx: DivinationContext, mapping: GodMapping) -> list[int]:
        """用神に該当する爻の位置リストを返す"""
        return [
            y.position for y in ctx.yao_list
            if y.liu_qin == mapping.yong_shen
        ]

    @staticmethod
    def find_fu_yong_shen(ctx: DivinationContext, mapping: GodMapping) -> list[int]:
        if mapping.fu_yong_shen is None:
            return []
        return [
            y.position for y in ctx.yao_list
            if y.liu_qin == mapping.fu_yong_shen
        ]


# ─────────────────────────────────────────────
# HomicideGateway�E�官鬼爻刁E���E�E
# ─────────────────────────────────────────────

@dataclass
class HomicideReport:
    """官鬼爻の動静・強弱レポ�EチE""
    guan_gui_positions: list[int]
    is_active:          bool   # 動爻 or 暗動
    is_strong:          bool   # 旺相
    is_broken:          bool   # 月破 or 日破
    threat_level:       int    # 0、E�E�高いほど危険�E�E
    description:        str


class HomicideGateway:
    """
    官鬼爻の動静を�E析する、E
    - 仕事占ぁE��官鬼が旺相・動爻 ↁE吁E
    - 健康・訴訟占ぁE��官鬼が旺相・動爻 ↁE凶�E�脅威大�E�E
    """

    @staticmethod
    def analyze(
        ctx: DivinationContext,
        analyses: list[YaoAnalysis],
        qtype: QuestionType,
    ) -> HomicideReport:
        guan_positions = [
            a.yao.position for a in analyses
            if a.yao.liu_qin == LiuQin.GUAN_GUI
        ]

        if not guan_positions:
            return HomicideReport(
                guan_gui_positions=[],
                is_active=False,
                is_strong=False,
                is_broken=False,
                threat_level=0,
                description="官鬼爻が卦中に伏す�E�伏神）。脅威�E潜在皁E��E,
            )

        # 最初�E官鬼爻を代表として使ぁE
        rep_pos = guan_positions[0]
        rep_analysis = next(a for a in analyses if a.yao.position == rep_pos)

        is_active  = rep_analysis.is_active
        is_strong  = is_wang_xiang(rep_analysis.wang_shuai)
        is_broken  = rep_analysis.is_po

        # 脁E��レベル計箁E
        threat = 0
        if is_active:  threat += 1
        if is_strong:  threat += 1
        if not is_broken: threat += 1  # 破砕されてぁE��ぁE��脁E��墁E

        # 質問タイプにより解釈反転
        if qtype in (QuestionType.CAREER, QuestionType.MARRIAGE, QuestionType.EXAM):
            # 官鬼が用祁EↁE強ぁE��ど吁E
            desc_parts = []
            if is_broken:
                desc_parts.append("官鬼爻は破砕されており力が失われてぁE���E��E�E�、E)
            elif is_active and is_strong:
                desc_parts.append("官鬼爻は旺相かつ動爻�E�暗動含む�E�、用神として強力（吉�E�、E)
            elif is_strong:
                desc_parts.append("官鬼爻は旺相だが静爻、力はあるが動かなぁE��E)
            else:
                desc_parts.append("官鬼爻は休囚・死、用神が弱ぁE���E�E�、E)
            desc = " ".join(desc_parts)
        else:
            # 官鬼が忌神（健康・失物など�E�E
            if is_broken:
                desc = "官鬼爻�E�忌神）�E破砕されており、脅威�E消滁E��吉�E�、E
            elif is_active and is_strong:
                desc = "官鬼爻�E�忌神）が旺相かつ動爻。最大の脁E��E��大凶�E�、E
            elif is_strong:
                desc = "官鬼爻�E�忌神）�E旺相だが静爻。潜在皁E��脁E��あり、E
            else:
                desc = "官鬼爻�E�忌神）�E休囚・死。脅威�E小さぁE��吉�E�、E

        return HomicideReport(
            guan_gui_positions=guan_positions,
            is_active=is_active,
            is_strong=is_strong,
            is_broken=is_broken,
            threat_level=threat,
            description=desc,
        )


# ─────────────────────────────────────────────
# DivinationEngine�E�統合エンジン�E�E
# ─────────────────────────────────────────────

class DivinationEngine:

    def __init__(self, ctx: DivinationContext, qtype: QuestionType):
        self.ctx   = ctx
        self.qtype = qtype

    def run(self) -> DivinationResult:
        # 1. 吁E��を�E极E
        analyses = [
            EnergyAnalyzer.analyze(y, self.ctx.yuejian, self.ctx.rizhen)
            for y in self.ctx.yao_list
        ]

        # 2. 用神�E副用神特宁E
        mapping          = TargetGodMapper.get_mapping(self.qtype)
        yong_positions   = TargetGodMapper.find_yong_shen(self.ctx, mapping)
        fu_positions     = TargetGodMapper.find_fu_yong_shen(self.ctx, mapping)
        yong_pos         = yong_positions[0] if yong_positions else self.ctx.shi_yao
        fu_pos           = fu_positions[0] if fu_positions else None

        # 3. 官鬼爻刁E��
        homicide_report  = HomicideGateway.analyze(self.ctx, analyses, self.qtype)

        # 4. 世爻・用神�Eスコアを集訁E
        yong_analysis    = next((a for a in analyses if a.yao.position == yong_pos), None)
        shi_analysis     = next((a for a in analyses if a.yao.position == self.ctx.shi_yao), None)

        score = 0
        if yong_analysis:
            score += yong_analysis.effective_strength
            if yong_analysis.is_po:
                score -= 3
        if shi_analysis:
            score += shi_analysis.effective_strength // 2

        # 官鬼の調整
        if self.qtype in (QuestionType.HEALTH, QuestionType.LOST_OBJECT):
            score -= homicide_report.threat_level
        elif self.qtype in (QuestionType.CAREER, QuestionType.MARRIAGE):
            score += (3 - homicide_report.threat_level) if homicide_report.is_broken else homicide_report.threat_level

        score = max(-10, min(score, 10))

        # 5. 判定文生�E
        verdict, detail = self._make_verdict(
            score, yong_analysis, homicide_report, mapping
        )

        return DivinationResult(
            context=self.ctx,
            yao_analyses=analyses,
            yong_shen_pos=yong_pos,
            fu_yong_shen_pos=fu_pos,
            verdict=verdict,
            detail=detail,
            score=score,
        )

    def _make_verdict(
        self,
        score: int,
        yong: Optional[YaoAnalysis],
        hom: HomicideReport,
        mapping: GodMapping,
    ) -> tuple[str, str]:
        if score >= 6:
            verdict = "大吁E
        elif score >= 3:
            verdict = "吁E
        elif score >= 1:
            verdict = "小吉"
        elif score == 0:
            verdict = "平"
        elif score >= -2:
            verdict = "小�E"
        elif score >= -5:
            verdict = "凶"
        else:
            verdict = "大凶"

        parts = [mapping.description]
        if yong:
            parts.append(yong.summary())
            if yong.is_po:
                parts.append("▶ 用神が破砕されてぁE��ため、事象は成就しがたい、E)
            if yong.an_dong:
                parts.append("▶ 用神が暗動�E�表面は静かだが�E部で動きが生じてぁE��、E)
        parts.append(hom.description)
        parts.append(f"総合スコア: {score:+d} ↁE判宁E {verdict}")

        return verdict, "\n".join(parts)


# ─────────────────────────────────────────────
# チE��トスイーチE
# ─────────────────────────────────────────────

def _make_yao(pos: int, lq: LiuQin, dz: DiZhi, state: YaoState = YaoState.STATIC) -> Yao:
    return Yao(position=pos, liu_qin=lq, di_zhi=dz, state=state)


class TestEnergyAnalyzerEdgeCases(unittest.TestCase):

    # ── 月破チE��チE──────────────────────────────
    def test_yue_po_basic(self):
        """子月に午爻 ↁE月破�E�子午相沖！E""
        yao = _make_yao(1, LiuQin.GUAN_GUI, DiZhi.WU)
        result = EnergyAnalyzer.analyze(yao, DiZhi.ZI, DiZhi.CHEN)
        self.assertTrue(result.yue_po)
        self.assertFalse(result.an_dong)
        self.assertEqual(result.effective_strength, -2)

    def test_yue_po_mao_you(self):
        """酉月に卯爻 ↁE月破"""
        yao = _make_yao(2, LiuQin.QI_CAI, DiZhi.MAO)
        result = EnergyAnalyzer.analyze(yao, DiZhi.YOU, DiZhi.HAI)
        self.assertTrue(result.yue_po)
        self.assertEqual(result.effective_strength, -2)

    def test_no_yue_po_non_chong(self):
        """子月に寁E�� ↁE月破なぁE""
        yao = _make_yao(1, LiuQin.ZI_SUN, DiZhi.YIN)
        result = EnergyAnalyzer.analyze(yao, DiZhi.ZI, DiZhi.CHEN)
        self.assertFalse(result.yue_po)

    # ── 日破チE��チE──────────────────────────────
    def test_ri_po_weak_static(self):
        """申日に寁E���E�休囚・静爻�E��E 日破�E�暗動なし！E""
        # 寁E�E木。申月なら木は死。でもここでは月建を別に設定、E
        # 子月に寁E�E木→旺相(XIANG)。申日と沖�E本来暗動のはず、E
        # 休囚死のケースを作るため、E��月（申月）に寁E��(木)を使ぁE��E
        # 申月：木=死 ↁE寁E�E申に相沖かつ死 ↁE日破
        yao = _make_yao(1, LiuQin.ZI_SUN, DiZhi.YIN, YaoState.STATIC)
        result = EnergyAnalyzer.analyze(yao, DiZhi.SHEN, DiZhi.SHEN)
        self.assertTrue(result.ri_po)
        self.assertFalse(result.an_dong)
        self.assertEqual(result.effective_strength, -2)

    def test_ri_po_dynamic_yao(self):
        """動爻が日辰に沖される ↁE日破�E�暗動にはならなぁE��E""
        yao = _make_yao(3, LiuQin.FU_MU, DiZhi.ZI, YaoState.DYNAMIC)
        # 子月�E�水は旺。日辰=午（子午沖！E
        result = EnergyAnalyzer.analyze(yao, DiZhi.ZI, DiZhi.WU)
        # 動爻なので暗動ではなく日破
        self.assertTrue(result.ri_po)
        self.assertFalse(result.an_dong)
        self.assertEqual(result.effective_strength, -2)

    # ── 暗動チE��チE──────────────────────────────
    def test_an_dong_basic(self):
        """旺相の静爻が日辰に沖される ↁE暗動"""
        # 子月�E�水旺�E�に子爻�E�水=旺�E�。日辰=午（子午沖）。静爻、E
        yao = _make_yao(4, LiuQin.XIONG_DI, DiZhi.ZI, YaoState.STATIC)
        result = EnergyAnalyzer.analyze(yao, DiZhi.ZI, DiZhi.WU)
        self.assertTrue(result.an_dong)
        self.assertFalse(result.ri_po)
        self.assertFalse(result.is_po)

    def test_an_dong_xiang(self):
        """相�E�次旺�E��E静爻が日辰に沖される ↁE暗動"""
        # 子月�E�水旺�E�に木爻�E�相�E�。卯爻を使ぁE��日辰=酉（卯酉沖）、E
        yao = _make_yao(2, LiuQin.ZI_SUN, DiZhi.MAO, YaoState.STATIC)
        result = EnergyAnalyzer.analyze(yao, DiZhi.ZI, DiZhi.YOU)
        ws = result.wang_shuai
        self.assertIn(ws, (WangShuai.WANG, WangShuai.XIANG))
        self.assertTrue(result.an_dong)

    def test_an_dong_not_xiu(self):
        """休（やめE���E��E静爻が日辰に沁EↁE日破�E�暗動でなぁE��E""
        # 水月（子月�E�に金爻�E�休）。申爻、日辰=寁E��寁E��沖）、E
        yao = _make_yao(1, LiuQin.GUAN_GUI, DiZhi.SHEN, YaoState.STATIC)
        result = EnergyAnalyzer.analyze(yao, DiZhi.ZI, DiZhi.YIN)
        ws = result.wang_shuai
        self.assertEqual(ws, WangShuai.XIU)
        self.assertTrue(result.ri_po)
        self.assertFalse(result.an_dong)

    def test_an_dong_strength_bonus(self):
        """暗動爻は旺衰ベ�Eス+1のボ�Eナスを得る"""
        yao = _make_yao(4, LiuQin.XIONG_DI, DiZhi.ZI, YaoState.STATIC)
        result = EnergyAnalyzer.analyze(yao, DiZhi.ZI, DiZhi.WU)
        # 旺(4) + 暗動(+1) = 5�E�破砕なし！E
        self.assertEqual(result.effective_strength, 5)

    # ── 月破�E�日沖（褁E���E�テスチE────────────────
    def test_yue_po_and_chong_ri(self):
        """月破爻が日辰にも沖される ↁE月破が優先、実効劁E-2"""
        # 午爻を子月�E�月破�E�かつ日辰=子（子午沖！E
        yao = _make_yao(1, LiuQin.QI_CAI, DiZhi.WU, YaoState.STATIC)
        result = EnergyAnalyzer.analyze(yao, DiZhi.ZI, DiZhi.ZI)
        self.assertTrue(result.yue_po)
        # 月破状態で日辰にも沖�E日破も�E立するかチェチE��
        # 火爻は子月で死、かつ日辰=子で沖�Eri_po
        self.assertTrue(result.ri_po or result.an_dong)  # ぁE��れかが�E竁E
        self.assertEqual(result.effective_strength, -2)

    # ── 日生テスチE──────────────────────────────
    def test_ri_sheng(self):
        """日辰が爻を生ずる場吁E+1"""
        # 木(寁E爻、日辰=亥(水)。水生木、E
        yao = _make_yao(1, LiuQin.ZI_SUN, DiZhi.YIN)
        result = EnergyAnalyzer.analyze(yao, DiZhi.ZI, DiZhi.HAI)
        self.assertTrue(result.ri_sheng)
        self.assertFalse(result.ri_ke)

    def test_ri_ke(self):
        """日辰が爻を剋す場吁E-1"""
        # 木(卯)爻、日辰=申(釁E。��剋木、E
        yao = _make_yao(1, LiuQin.ZI_SUN, DiZhi.MAO)
        result = EnergyAnalyzer.analyze(yao, DiZhi.ZI, DiZhi.SHEN)
        self.assertFalse(result.ri_sheng)
        self.assertTrue(result.ri_ke)


class TestTargetGodMapper(unittest.TestCase):

    def test_career_mapping(self):
        m = TargetGodMapper.get_mapping(QuestionType.CAREER)
        self.assertEqual(m.yong_shen, LiuQin.GUAN_GUI)
        self.assertEqual(m.fu_yong_shen, LiuQin.FU_MU)

    def test_health_mapping(self):
        m = TargetGodMapper.get_mapping(QuestionType.HEALTH)
        self.assertEqual(m.yong_shen, LiuQin.ZI_SUN)
        self.assertIsNone(m.fu_yong_shen)

    def test_find_yong_shen_in_context(self):
        ctx = DivinationContext(
            yao_list=[
                _make_yao(1, LiuQin.XIONG_DI, DiZhi.ZI),
                _make_yao(2, LiuQin.GUAN_GUI, DiZhi.YIN),
                _make_yao(3, LiuQin.ZI_SUN,   DiZhi.MAO),
                _make_yao(4, LiuQin.QI_CAI,   DiZhi.SI),
                _make_yao(5, LiuQin.FU_MU,    DiZhi.WEI),
                _make_yao(6, LiuQin.GUAN_GUI, DiZhi.YOU),
            ],
            yuejian=DiZhi.ZI, rizhen=DiZhi.CHEN,
            shi_yao=1, ying_yao=4,
        )
        m = TargetGodMapper.get_mapping(QuestionType.CAREER)
        positions = TargetGodMapper.find_yong_shen(ctx, m)
        self.assertIn(2, positions)
        self.assertIn(6, positions)


class TestHomicideGateway(unittest.TestCase):

    def _make_context_with_guan(
        self, guan_dz: DiZhi, guan_state: YaoState,
        yuejian: DiZhi, rizhen: DiZhi
    ) -> tuple[DivinationContext, list[YaoAnalysis]]:
        yao_list = [
            _make_yao(1, LiuQin.XIONG_DI,  DiZhi.ZI),
            _make_yao(2, LiuQin.GUAN_GUI,  guan_dz, guan_state),
            _make_yao(3, LiuQin.ZI_SUN,    DiZhi.MAO),
            _make_yao(4, LiuQin.QI_CAI,    DiZhi.SI),
            _make_yao(5, LiuQin.FU_MU,     DiZhi.WEI),
            _make_yao(6, LiuQin.XIONG_DI,  DiZhi.YOU),
        ]
        ctx = DivinationContext(
            yao_list=yao_list,
            yuejian=yuejian, rizhen=rizhen,
            shi_yao=1, ying_yao=4,
        )
        analyses = [EnergyAnalyzer.analyze(y, yuejian, rizhen) for y in yao_list]
        return ctx, analyses

    def test_guan_gui_active_health_is_dangerous(self):
        """健康占�E�官鬼が旺相・動爻 ↁE脁E��大"""
        ctx, analyses = self._make_context_with_guan(
            DiZhi.YIN, YaoState.DYNAMIC, DiZhi.ZI, DiZhi.CHEN
        )
        report = HomicideGateway.analyze(ctx, analyses, QuestionType.HEALTH)
        self.assertGreaterEqual(report.threat_level, 2)

    def test_guan_gui_broken_health_is_safe(self):
        """健康占�E�官鬼が月破 ↁE脁E��消滁E""
        # 子月、官鬼=午（子午沖）�E月破
        ctx, analyses = self._make_context_with_guan(
            DiZhi.WU, YaoState.STATIC, DiZhi.ZI, DiZhi.CHEN
        )
        report = HomicideGateway.analyze(ctx, analyses, QuestionType.HEALTH)
        self.assertTrue(report.is_broken)
        self.assertIn("消滁E, report.description)

    def test_guan_gui_empty(self):
        """官鬼爻が卦中になぁE��吁E""
        yao_list = [
            _make_yao(1, LiuQin.XIONG_DI, DiZhi.ZI),
            _make_yao(2, LiuQin.ZI_SUN,   DiZhi.YIN),
            _make_yao(3, LiuQin.QI_CAI,   DiZhi.MAO),
            _make_yao(4, LiuQin.FU_MU,    DiZhi.SI),
            _make_yao(5, LiuQin.XIONG_DI, DiZhi.WEI),
            _make_yao(6, LiuQin.QI_CAI,   DiZhi.YOU),
        ]
        ctx = DivinationContext(
            yao_list=yao_list,
            yuejian=DiZhi.ZI, rizhen=DiZhi.CHEN,
            shi_yao=1, ying_yao=4,
        )
        analyses = [EnergyAnalyzer.analyze(y, DiZhi.ZI, DiZhi.CHEN) for y in yao_list]
        report = HomicideGateway.analyze(ctx, analyses, QuestionType.HEALTH)
        self.assertEqual(report.guan_gui_positions, [])
        self.assertIn("伏す", report.description)


class TestDivinationEngine(unittest.TestCase):

    def _make_career_context(self) -> DivinationContext:
        return DivinationContext(
            yao_list=[
                _make_yao(1, LiuQin.XIONG_DI,  DiZhi.ZI),
                _make_yao(2, LiuQin.GUAN_GUI,  DiZhi.YIN, YaoState.DYNAMIC),
                _make_yao(3, LiuQin.ZI_SUN,    DiZhi.MAO),
                _make_yao(4, LiuQin.QI_CAI,    DiZhi.SI),
                _make_yao(5, LiuQin.FU_MU,     DiZhi.WEI),
                _make_yao(6, LiuQin.XIONG_DI,  DiZhi.YOU),
            ],
            yuejian=DiZhi.ZI,   # 子月�E�水旺�E�E
            rizhen=DiZhi.CHEN,
            shi_yao=1, ying_yao=4,
        )

    def test_career_positive(self):
        """仕事占�E�官鬼爻が旺相かつ動爻 ↁE吉寁E��"""
        ctx = self._make_career_context()
        engine = DivinationEngine(ctx, QuestionType.CAREER)
        result = engine.run()
        # 官鬼=寁E木), 子月(水)→木は相。動爻 ↁE用神が強ぁE
        self.assertGreater(result.score, 0)

    def test_career_yong_po_is_bad(self):
        """仕事占�E�用神（官鬼�E�が月破 ↁE凶"""
        ctx = DivinationContext(
            yao_list=[
                _make_yao(1, LiuQin.XIONG_DI,  DiZhi.ZI),
                _make_yao(2, LiuQin.GUAN_GUI,  DiZhi.WU),   # 子月→月破
                _make_yao(3, LiuQin.ZI_SUN,    DiZhi.MAO),
                _make_yao(4, LiuQin.QI_CAI,    DiZhi.SI),
                _make_yao(5, LiuQin.FU_MU,     DiZhi.WEI),
                _make_yao(6, LiuQin.XIONG_DI,  DiZhi.YOU),
            ],
            yuejian=DiZhi.ZI, rizhen=DiZhi.CHEN,
            shi_yao=1, ying_yao=4,
        )
        engine = DivinationEngine(ctx, QuestionType.CAREER)
        result = engine.run()
        self.assertLess(result.score, 0)

    def test_health_strong_guan_is_bad(self):
        """健康占�E�官鬼が旺相動爻、用神（子孫�E�が月破 ↁE凶�E�病邪強ぁE�E治癒力消滁E��E""
        # 子月。子孫爻=午（子午沖�E月破�E�。官鬼=寁E��木、相�E�動爻、E
        ctx = DivinationContext(
            yao_list=[
                _make_yao(1, LiuQin.ZI_SUN,    DiZhi.WU),   # 月破�E�子午沖！E
                _make_yao(2, LiuQin.GUAN_GUI,  DiZhi.YIN, YaoState.DYNAMIC),
                _make_yao(3, LiuQin.QI_CAI,    DiZhi.MAO),
                _make_yao(4, LiuQin.XIONG_DI,  DiZhi.SI),
                _make_yao(5, LiuQin.FU_MU,     DiZhi.WEI),
                _make_yao(6, LiuQin.QI_CAI,    DiZhi.YOU),
            ],
            yuejian=DiZhi.ZI, rizhen=DiZhi.CHEN,
            shi_yao=3, ying_yao=6,
        )
        engine = DivinationEngine(ctx, QuestionType.HEALTH)
        result = engine.run()
        # 用神が月破(-2)、官鬼脁E��大(-3) ↁE合計で負になる�EぁE
        self.assertLess(result.score, 0)

    def test_wealth_yong_shen_is_qi_cai(self):
        """財運占�E�用神が妻財爻であることを確誁E""
        ctx = DivinationContext(
            yao_list=[
                _make_yao(1, LiuQin.XIONG_DI,  DiZhi.ZI),
                _make_yao(2, LiuQin.GUAN_GUI,  DiZhi.YIN),
                _make_yao(3, LiuQin.ZI_SUN,    DiZhi.MAO),
                _make_yao(4, LiuQin.QI_CAI,    DiZhi.SI, YaoState.DYNAMIC),
                _make_yao(5, LiuQin.FU_MU,     DiZhi.WEI),
                _make_yao(6, LiuQin.QI_CAI,    DiZhi.YOU),
            ],
            yuejian=DiZhi.ZI, rizhen=DiZhi.CHEN,
            shi_yao=1, ying_yao=4,
        )
        engine = DivinationEngine(ctx, QuestionType.WEALTH)
        result = engine.run()
        yong_yao = next(a for a in result.yao_analyses if a.yao.position == result.yong_shen_pos)
        self.assertEqual(yong_yao.yao.liu_qin, LiuQin.QI_CAI)


# ─────────────────────────────────────────────
# チE��出劁E
# ─────────────────────────────────────────────

def demo():
    print("=" * 60)
    print("  六爻占術判定エンジン チE��")
    print("=" * 60)

    # シナリオ�E�仕事占ぁE
    # 子月・辰日。官鬼爻�E�寁E��が2爻で動爻。世爻=1爻、E
    ctx = DivinationContext(
        yao_list=[
            _make_yao(1, LiuQin.XIONG_DI,  DiZhi.ZI),
            _make_yao(2, LiuQin.GUAN_GUI,  DiZhi.YIN, YaoState.DYNAMIC),
            _make_yao(3, LiuQin.ZI_SUN,    DiZhi.MAO),
            _make_yao(4, LiuQin.QI_CAI,    DiZhi.SI),
            _make_yao(5, LiuQin.FU_MU,     DiZhi.WEI),
            _make_yao(6, LiuQin.XIONG_DI,  DiZhi.YOU),
        ],
        yuejian=DiZhi.ZI,
        rizhen=DiZhi.CHEN,
        shi_yao=1,
        ying_yao=4,
    )

    engine = DivinationEngine(ctx, QuestionType.CAREER)
    result = engine.run()

    print(f"\n質問タイチE {QuestionType.CAREER.value}")
    print(f"月建: {ctx.yuejian.name}  日辰: {ctx.rizhen.name}")
    print(f"世爻: {ctx.shi_yao}爻  用神位置: {result.yong_shen_pos}爻\n")
    print("─ 吁E��の刁E�� ─")
    for a in result.yao_analyses:
        print(" ", a.summary())
    print()
    print("─ 占断結果 ─")
    print(result.detail)
    print()
    print(f"☁E最終判宁E {result.verdict}  (スコア {result.score:+d})")
    print()

    # 暗動シナリオ
    print("=" * 60)
    print("  暗動シナリオ�E�旺相静爻が日辰に沖される")
    print("=" * 60)
    yao = _make_yao(4, LiuQin.GUAN_GUI, DiZhi.ZI, YaoState.STATIC)
    ana = EnergyAnalyzer.analyze(yao, DiZhi.ZI, DiZhi.WU)
    print(ana.summary())
    print()

    # 月破シナリオ
    print("=" * 60)
    print("  月破シナリオ�E�子月に午爻")
    print("=" * 60)
    yao2 = _make_yao(2, LiuQin.QI_CAI, DiZhi.WU, YaoState.STATIC)
    ana2 = EnergyAnalyzer.analyze(yao2, DiZhi.ZI, DiZhi.CHEN)
    print(ana2.summary())


# ─────────────────────────────────────────────
# エントリーポインチE
# ─────────────────────────────────────────────

if __name__ == "__main__":
    import sys
    if "--test" in sys.argv:
        sys.argv.remove("--test")
        loader = unittest.TestLoader()
        suite  = unittest.TestSuite()
        for cls in [
            TestEnergyAnalyzerEdgeCases,
            TestTargetGodMapper,
            TestHomicideGateway,
            TestDivinationEngine,
        ]:
            suite.addTests(loader.loadTestsFromTestCase(cls))
        runner = unittest.TextTestRunner(verbosity=2)
        result = runner.run(suite)
        sys.exit(0 if result.wasSuccessful() else 1)
    else:
        demo()


# ════════════════════════════════════════════════════════════════╁E
# PHASE 2: 種本統合モジュール
# ════════════════════════════════════════════════════════════════╁E

# ─────────────────────────────────────────────
# 十二長生（長生�E沐浴・冠帯・臨官�E帝旺・衰・痁E�E死・墓�E絶・胎�E養！E
# 吁E��行�Eどの地支が「墓」「絶」「死」に当たるか
# ─────────────────────────────────────────────

# 五行ごとの「墓地」（�E墓）地支
MU_DI: dict[GoXing, DiZhi] = {
    GoXing.WOOD:  DiZhi.WEI,   # 木の墁E= 未
    GoXing.FIRE:  DiZhi.XU,    # 火の墁E= 戁E
    GoXing.EARTH: DiZhi.XU,    # 土�E墁E= 戌（火土同墓！E
    GoXing.METAL: DiZhi.CHOU,  # 金�E墁E= 丁E
    GoXing.WATER: DiZhi.CHEN,  # 水の墁E= 辰
}

# 五行ごとの「絶地」地支�E�長生�E対沖！E
JUE_DI: dict[GoXing, DiZhi] = {
    GoXing.WOOD:  DiZhi.SHEN,  # 木絶 = 申
    GoXing.FIRE:  DiZhi.HAI,   # 火絶 = 亥
    GoXing.EARTH: DiZhi.HAI,   # 土絶 = 亥
    GoXing.METAL: DiZhi.YIN,   # 金絶 = 寁E
    GoXing.WATER: DiZhi.SI,    # 水絶 = 巳
}

# 五行ごとの「死地」地支
SI_DI: dict[GoXing, DiZhi] = {
    GoXing.WOOD:  DiZhi.WU,    # 木死 = 十E
    GoXing.FIRE:  DiZhi.YOU,   # 火死 = 酁E
    GoXing.EARTH: DiZhi.YOU,   # 土死 = 酁E
    GoXing.METAL: DiZhi.ZI,    # 金死 = 孁E
    GoXing.WATER: DiZhi.MAO,   # 水死 = 卯
}


def is_ru_mu(yao_wx: GoXing, dz: DiZhi) -> bool:
    """yao_wx の五行が地支 dz に入墓するか"""
    return MU_DI.get(yao_wx) == dz


def is_jue_di(yao_wx: GoXing, dz: DiZhi) -> bool:
    """yao_wx の五行が地支 dz で絶地ぁE""
    return JUE_DI.get(yao_wx) == dz


def is_si_di(yao_wx: GoXing, dz: DiZhi) -> bool:
    """yao_wx の五行が地支 dz で死地ぁE""
    return SI_DI.get(yao_wx) == dz


# 五行物質属性辞書�E�種本の根本思想2�E�E
WUXING_MATERIAL: dict[GoXing, dict] = {
    GoXing.FIRE: {
        "物質": ["熱", "炁E, "允E, "電氁E, "太陽"],
        "臓器": ["忁E��", "小�E", "神絁E],
        "現象": ["燁E��", "感情爁E��", "急速な変化"],
    },
    GoXing.WOOD: {
        "物質": ["植物", "木杁E, "繊維"],
        "臓器": ["肝臓", "胁E��", "神経系"],
        "現象": ["成長", "発屁E, "方向転揁E],
    },
    GoXing.EARTH: {
        "物質": ["大地", "コンクリーチE, "プラスチック", "陶器"],
        "臓器": ["胁E, "脾臁E, "筋肉"],
        "現象": ["安宁E, "重力", "物質匁E],
    },
    GoXing.METAL: {
        "物質": ["金屁E, "刁E��", "精寁E��械", "鉱石"],
        "臓器": ["肺", "大腸", "呼吸器"],
        "現象": ["収縮", "制陁E, "刁E��", "精寁E],
    },
    GoXing.WATER: {
        "物質": ["水", "液佁E, "氷", "油"],
        "臓器": ["腎臓", "膀胱", "骨髁E],
        "現象": ["流動", "浸送E, "冷却", "融解"],
    },
}


# ─────────────────────────────────────────────
# 回頭の甁E検�Eエンジン�E�EuiTouSheng�E�E
# ─────────────────────────────────────────────

@dataclass
class HuiTouShengResult:
    """回頭の生�E検�E結果"""
    detected:      bool
    source_yao:    int         # 動爻の位置
    hua_chu_wx:    GoXing      # 化�Eした五衁E
    target_yao:    int         # 恩恵を受ける爻の位置
    target_wx:     GoXing      # 恩恵を受ける爻の五衁E
    description:   str


class HuiTouShengDetector:
    """
    回頭の生（危機�E反転�E�検�E、E

    允E��が化出先�E五行に変化した後、E
    そ�E化�E先がさらに「目皁E���E�世爻 or 用神）」を
    生じる流れになる場吁E= 回頭の生、E

    例：火(動爻) ↁE圁E化�E) ↁE土生釁E目皁E��)
        一見困難な動爻が、最終的に目皁E��助ける、E
    """

    @staticmethod
    def detect(
        ctx: DivinationContext,
        analyses: list[YaoAnalysis],
        target_pos: int,
    ) -> list[HuiTouShengResult]:
        results: list[HuiTouShengResult] = []
        target_a = next((a for a in analyses if a.yao.position == target_pos), None)
        if target_a is None:
            return results
        target_wx = target_a.yao.wuxing

        for a in analyses:
            yao = a.yao
            if yao.state != YaoState.DYNAMIC or yao.bian_zhi is None:
                continue
            hua_wx = wuxing_of(yao.bian_zhi)
            # 化�Eした五行が目皁E��の五行を生じるか
            if EnergyAnalyzer._sheng(hua_wx, target_wx):
                # さらに允E��が目皁E��を直接剋してぁE��ぁE��純粋な回頭�E�また�E
                # 剋してぁE��も化出で相殺�E�送E���E�してぁE��場合も検�E
                desc_parts = [
                    f"{yao.position}爻({yao.wuxing.value}→{hua_wx.value})が化出し、E,
                    f"{hua_wx.value}が{target_pos}爻({target_wx.value})を生じる、E,
                ]
                if EnergyAnalyzer._ke(yao.wuxing, target_wx):
                    desc_parts.append("允E��は剋�E関係だったが化�Eにより生に転じる【真の回頭の生】、E)
                else:
                    desc_parts.append("化�E後に生�E連鎖が形成される【化出の生】、E)
                results.append(HuiTouShengResult(
                    detected=True,
                    source_yao=yao.position,
                    hua_chu_wx=hua_wx,
                    target_yao=target_pos,
                    target_wx=target_wx,
                    description="".join(desc_parts),
                ))
        return results


# ─────────────────────────────────────────────
# 変爻・進神�E退祁E刁E���E�EianYaoAnalyzer�E�E
# ─────────────────────────────────────────────

# 十二地支の頁E��インチE��クス�E�E=子、E1=亥�E��Eすでに DiZhi.value で定義済み

# 五行ごとの帝旺地支�E�最も強ぁE��支�E�E
DI_WANG: dict[GoXing, DiZhi] = {
    GoXing.WOOD:  DiZhi.MAO,   # 木帝旺 = 卯(3)
    GoXing.FIRE:  DiZhi.WU,    # 火帝旺 = 十E6)
    GoXing.EARTH: DiZhi.WU,    # 土帝旺 = 十E6)�E�火土同旺�E�E
    GoXing.METAL: DiZhi.YOU,   # 金帝旺 = 酁E9)
    GoXing.WATER: DiZhi.ZI,    # 水帝旺 = 孁E0)
}


def _dizhi_dist_to_wang(dz: DiZhi, wx: GoXing) -> int:
    """地支 dz から帝旺までの十二支頁E��向�E距離�E�E、E1�E�。小さぁE��ど帝旺に近い、E""
    wang = DI_WANG[wx]
    return (wang.value - dz.value) % 12


def is_jin_shen(original: DiZhi, bian: DiZhi) -> bool:
    """
    進神：変爻が�E爻より帝旺に近い方向（より強ぁE��支�E�に移行する、E
    同じ五行であること�E�同気前進�E�、E
    例：水: 亥→子（亥は距離1、子�E距離0=帝旺�E��E 進祁E
        木: 寁E�E卯�E�寁E�E距離1、卯は距離0=帝旺�E��E 進祁E
    """
    if DIZHI_WUXING[original] != DIZHI_WUXING[bian]:
        return False
    wx = DIZHI_WUXING[original]
    return _dizhi_dist_to_wang(bian, wx) < _dizhi_dist_to_wang(original, wx)


def is_tui_shen(original: DiZhi, bian: DiZhi) -> bool:
    """
    退神：変爻が�E爻より帝旺から遠ざかる方向（より弱ぁE��支�E�に移行する、E
    同じ五行であること、E
    例：水: 子�E亥�E�子�E距離0=帝旺、亥は距離1�E��E 退祁E
        木: 卯→寁E��卯は距離0=帝旺、寁E�E距離1�E��E 退祁E
    """
    if DIZHI_WUXING[original] != DIZHI_WUXING[bian]:
        return False
    wx = DIZHI_WUXING[original]
    return _dizhi_dist_to_wang(bian, wx) > _dizhi_dist_to_wang(original, wx)


@dataclass
class BianYaoAnalysis:
    """動爻の変化方向�E极E""
    yao_pos:     int
    original_dz: DiZhi
    bian_dz:     DiZhi
    hua_wx:      GoXing    # 化�Eした五衁E
    is_jin:      bool      # 進祁E
    is_tui:      bool      # 退祁E
    ru_mu_bian:  bool      # 化�E先が入墓地支か（目皁E��基準！E
    description: str


class BianYaoAnalyzer:

    @staticmethod
    def analyze_all(ctx: DivinationContext) -> list[BianYaoAnalysis]:
        results = []
        for yao in ctx.yao_list:
            if yao.state != YaoState.DYNAMIC or yao.bian_zhi is None:
                continue
            hua_wx = wuxing_of(yao.bian_zhi)
            jin = is_jin_shen(yao.di_zhi, yao.bian_zhi)
            tui = is_tui_shen(yao.di_zhi, yao.bian_zhi)
            # 化�Eが�E爻五行�E墓地に入るか
            ru_mu = is_ru_mu(yao.wuxing, yao.bian_zhi)
            parts = [f"{yao.position}爻 {yao.di_zhi.name}→{yao.bian_zhi.name}({hua_wx.value}): "]
            if jin:
                parts.append("進神（前進・増強�E�E)
            elif tui:
                parts.append("退神（後退・衰退確定！E)
            else:
                parts.append("化�E�E�五行変化�E�E)
            if ru_mu:
                parts.append(" ☁E�E墓化出�E�エネルギー消滁E��E)
            results.append(BianYaoAnalysis(
                yao_pos=yao.position,
                original_dz=yao.di_zhi,
                bian_dz=yao.bian_zhi,
                hua_wx=hua_wx,
                is_jin=jin,
                is_tui=tui,
                ru_mu_bian=ru_mu,
                description="".join(parts),
            ))
        return results


# ─────────────────────────────────────────────
# 伏神技法！EuShenAnalyzer�E�E
# ─────────────────────────────────────────────

# 八宮首卦の六爻地支定義�E�純卦の地支配�E: position 1、E�E�E
# 吁E��の「本宮卦」（乾・兌�E離・霁E�E巽・坎�E艮・坤�E�E
# の地支は長生表から導�E。ここでは標準的な斁E��後天配置を使用、E
GONG_SHOU_GUA: dict[str, list[DiZhi]] = {
    "乾": [DiZhi.ZI, DiZhi.YIN, DiZhi.CHEN, DiZhi.WU, DiZhi.SHEN, DiZhi.XU],
    "允E: [DiZhi.SI, DiZhi.WEI, DiZhi.YOU, DiZhi.HAI, DiZhi.CHOU, DiZhi.MAO],
    "離": [DiZhi.MAO, DiZhi.SI, DiZhi.WEI, DiZhi.YOU, DiZhi.HAI, DiZhi.CHOU],
    "霁E: [DiZhi.ZI, DiZhi.YIN, DiZhi.CHEN, DiZhi.WU, DiZhi.SHEN, DiZhi.XU],
    "巽": [DiZhi.CHOU, DiZhi.HAI, DiZhi.YOU, DiZhi.WEI, DiZhi.SI, DiZhi.MAO],
    "坁E: [DiZhi.YIN, DiZhi.CHEN, DiZhi.WU, DiZhi.SHEN, DiZhi.XU, DiZhi.ZI],
    "艮": [DiZhi.CHEN, DiZhi.YIN, DiZhi.ZI, DiZhi.XU, DiZhi.SHEN, DiZhi.WU],
    "坤": [DiZhi.WEI, DiZhi.SI, DiZhi.MAO, DiZhi.CHOU, DiZhi.HAI, DiZhi.YOU],
}


@dataclass
class FuShenResult:
    """伏神�E析結果"""
    fu_yao_pos:    int        # 伏神が伏す爻の位置�E�飛神�E位置�E�E
    fu_liu_qin:    LiuQin    # 伏神�E六親
    fu_dz:         DiZhi     # 伏神�E地支
    fu_wx:         GoXing    # 伏神�E五衁E
    fei_shen_dz:   DiZhi     # 飛神�E地支
    fei_shen_wx:   GoXing    # 飛神�E五衁E
    fei_ke_fu:     bool      # 飛神が伏神を剋す�E��E伏困難�E�E
    fei_sheng_fu:  bool      # 飛神が伏神を生ず�E��E伏容易！E
    can_emerge:    bool      # 出伏可能ぁE
    description:   str


class FuShenAnalyzer:
    """
    用神が表卦に出現しなぁE��合、宮の首卦から伏神を抽出する、E
    飛神（表卦の同位置爻�E�との相克関係で「�E伏」可否を判定、E
    """

    @staticmethod
    def find(
        ctx: DivinationContext,
        target_liu_qin: LiuQin,
        gong: str,
    ) -> Optional[FuShenResult]:
        """
        target_liu_qin が表卦に存在しなぁE��合、E
        宮の首卦からそ�E六親に対応する地支を伏神として抽出、E
        """
        # 表卦に存在するか確誁E
        present = [y for y in ctx.yao_list if y.liu_qin == target_liu_qin]
        if present:
            return None  # 伏神不要E

        shou_gua = GONG_SHOU_GUA.get(gong)
        if shou_gua is None:
            return None

        # 首卦から同じ六親に対応する爻を探す（簡易実裁E��五行が一致する位置を探す！E
        # 実際の六親は宮により異なるが、ここでは首卦の地支五行かめE
        # 用神�E五行！EargetGodMapper由来�E�で最初にヒットする位置を使ぁE
        mapping = QUESTION_GOD_MAP.get(QuestionType.CAREER)  # ダミ�E
        # 実際の呼び出し�Eから liu_qin の五行候補を絞る
        # ↁE首卦で用神�E六親と同じ六親になり得る地支を探ぁE

        # 簡易実裁E��首卦の吁E��置を�Eめて、E
        # 表卦の同位置爻�E�飛神）との関係を算�E
        # 用神�E親に対応する五行セチE��を暗黙的に使ぁE
        for pos_idx, fu_dz in enumerate(shou_gua):
            pos = pos_idx + 1
            fu_wx = wuxing_of(fu_dz)
            # 飛神（表卦の同位置�E�E
            fei_yao = next((y for y in ctx.yao_list if y.position == pos), None)
            if fei_yao is None:
                continue
            fei_wx = fei_yao.wuxing
            fei_ke_fu  = EnergyAnalyzer._ke(fei_wx, fu_wx)
            fei_sheng_fu = EnergyAnalyzer._sheng(fei_wx, fu_wx)
            can_emerge = fei_sheng_fu or (not fei_ke_fu)

            # 六親判定（宮・世爻・用神�E関係から送E��！E
            # 簡易：首卦の地支五行が用神�E親の五行帯に属するかをチェチE��
            # 実裁E��は target_liu_qin の典型的五行を参�E
            liu_qin_wx_map: dict[LiuQin, list[GoXing]] = {
                LiuQin.GUAN_GUI: [GoXing.METAL, GoXing.WOOD, GoXing.FIRE, GoXing.WATER, GoXing.EARTH],
                LiuQin.QI_CAI:   [GoXing.METAL, GoXing.WOOD, GoXing.FIRE, GoXing.WATER, GoXing.EARTH],
                LiuQin.ZI_SUN:   [GoXing.METAL, GoXing.WOOD, GoXing.FIRE, GoXing.WATER, GoXing.EARTH],
                LiuQin.FU_MU:    [GoXing.METAL, GoXing.WOOD, GoXing.FIRE, GoXing.WATER, GoXing.EARTH],
                LiuQin.XIONG_DI: [GoXing.METAL, GoXing.WOOD, GoXing.FIRE, GoXing.WATER, GoXing.EARTH],
            }
            desc_parts = [
                f"伏祁E {fu_dz.name}({fu_wx.value}) ぁE{pos}爻 飛祁E{fei_yao.di_zhi.name}({fei_wx.value})の下に伏す、E"
            ]
            if fei_ke_fu:
                desc_parts.append("飛神が伏神を剋す ↁE出伏困難�E�発見�E解決が難しい�E�、E)
            elif fei_sheng_fu:
                desc_parts.append("飛神が伏神を生ず ↁE出伏容易（発見�E解決の好機あり）、E)
            else:
                desc_parts.append("飛神と伏神�E比和 or 無関俁EↁE出伏�E月日次第、E)

            return FuShenResult(
                fu_yao_pos=pos,
                fu_liu_qin=target_liu_qin,
                fu_dz=fu_dz,
                fu_wx=fu_wx,
                fei_shen_dz=fei_yao.di_zhi,
                fei_shen_wx=fei_wx,
                fei_ke_fu=fei_ke_fu,
                fei_sheng_fu=fei_sheng_fu,
                can_emerge=can_emerge,
                description="".join(desc_parts),
            )
        return None


# ─────────────────────────────────────────────
# 他殺判定ゲートウェイ�E�拡張版！E
# ─────────────────────────────────────────────

@dataclass
class HomicideJudgment:
    """他殺か事故死か病死かを判宁E""
    guan_is_dynamic:    bool   # 官鬼爻が動爻ぁE
    guan_is_strong:     bool   # 官鬼爻が旺相ぁE
    guan_is_broken:     bool   # 官鬼爻が破砕か
    verdict:            str    # "他殺疑い" / "痁E��・事故" / "不�E"
    confidence:         str    # "確宁E / "有力" / "弱ぁE
    description:        str


class HomicideJudgmentGateway:
    """
    種本の根本思想 3�E�E
    「官鬼が動爻として発動してぁE��か否か」が他殺判定�E絶対基準、E
    動爻なぁEↁE外部の人為皁E��害は100%否定、E
    動爻あり ↁE外部加害の可能性あり、E
    """

    @staticmethod
    def judge(analyses: list[YaoAnalysis]) -> HomicideJudgment:
        guan_analyses = [a for a in analyses if a.yao.liu_qin == LiuQin.GUAN_GUI]

        if not guan_analyses:
            return HomicideJudgment(
                guan_is_dynamic=False,
                guan_is_strong=False,
                guan_is_broken=False,
                verdict="痁E��・事故",
                confidence="有力",
                description="官鬼爻が卦中に不在�E�伏神）。外部加害老E�E痕跡なし。病死・自然死の可能性が高い、E,
            )

        rep = guan_analyses[0]
        is_dynamic = rep.yao.state == YaoState.DYNAMIC or rep.an_dong
        is_strong  = is_wang_xiang(rep.wang_shuai)
        is_broken  = rep.is_po

        if not is_dynamic:
            verdict     = "痁E��・事故"
            confidence  = "確宁E
            desc = (
                "官鬼爻は静爻�E�暗動もなし）、E
                "外部からの人為皁E��害は存在しなぁE��E
                "事故死・痁E��・自然現象と断定、E
            )
        elif is_dynamic and is_strong and not is_broken:
            verdict     = "他殺疑い"
            confidence  = "有力"
            desc = (
                "官鬼爻が旺相かつ動爻�E�また�E暗動�E�、E
                "外部からの強ぁE��害皁E��ネルギーが確認される、E
                "他殺・外部加害の可能性を排除できなぁE��E
            )
        elif is_dynamic and is_broken:
            verdict     = "痁E��・事故"
            confidence  = "有力"
            desc = (
                "官鬼爻は動爻だが破砕されてぁE��、E
                "加害皁E��ネルギーは存在したが無効化された、E
                "事故皁E��素はあるが意図皁E��害とは言えなぁE��E
            )
        else:
            verdict     = "不�E"
            confidence  = "弱ぁE
            desc = (
                "官鬼爻は動爻だが休囚死の状態、E
                "外部影響は弱く、状況�E褁E��皁E��追加刁E��が忁E��、E
            )

        return HomicideJudgment(
            guan_is_dynamic=is_dynamic,
            guan_is_strong=is_strong,
            guan_is_broken=is_broken,
            verdict=verdict,
            confidence=confidence,
            description=desc,
        )


# ─────────────────────────────────────────────
# 応期計算！EingQiCalculator�E�E
# ─────────────────────────────────────────────

@dataclass
class YingQiResult:
    """吉�E発現時期の予測"""
    target_wx:          GoXing
    best_dizhi:         list[DiZhi]   # 吉事�E応期地支
    worst_dizhi:        list[DiZhi]   # 凶事�E応期地支
    current_status:     str           # 現在の月日に対する評価
    description:        str


class YingQiCalculator:
    """
    応期�E�吉事�E凶事がぁE��発現するか�E時間軸計算、E

    吉事�E応期 = 用神が月日に生じられる、また�E旺相になる時
    凶事�E応期 = 用神が月日に剋される、また�E墓�E絶に入る時
    他殺発現朁E= 官鬼が月日に旺相になる時
    """

    @staticmethod
    def calc(
        target_wx: GoXing,
        yuejian: DiZhi,
        rizhen: DiZhi,
    ) -> YingQiResult:
        # 吉�E応期�E�目皁E��を生ずる五行�E地支、また�E比和
        def generates_target(dz: DiZhi) -> bool:
            return EnergyAnalyzer._sheng(wuxing_of(dz), target_wx)

        def same_wx(dz: DiZhi) -> bool:
            return wuxing_of(dz) == target_wx

        def kills_target(dz: DiZhi) -> bool:
            return EnergyAnalyzer._ke(wuxing_of(dz), target_wx)

        def is_tomb(dz: DiZhi) -> bool:
            return is_ru_mu(target_wx, dz)

        def is_jue(dz: DiZhi) -> bool:
            return is_jue_di(target_wx, dz)

        all_dz = list(DiZhi)
        best   = [dz for dz in all_dz if generates_target(dz) or same_wx(dz)]
        worst  = [dz for dz in all_dz if kills_target(dz) or is_tomb(dz) or is_jue(dz)]

        # 現在の評価
        curr_parts = []
        if generates_target(yuejian):
            curr_parts.append(f"月建({yuejian.name})が{target_wx.value}を生ぁEↁE月生�E�吉背景�E�、E)
        elif kills_target(yuejian):
            curr_parts.append(f"月建({yuejian.name})が{target_wx.value}を剋ぁEↁE月剋�E��E背景�E�、E)
        elif is_ru_mu(target_wx, yuejian):
            curr_parts.append(f"月建({yuejian.name})が{target_wx.value}の墁EↁE月墓（深刻�E�、E)

        if generates_target(rizhen):
            curr_parts.append(f"日辰({rizhen.name})が{target_wx.value}を生ぁEↁE日生（当日吉）、E)
        elif kills_target(rizhen):
            curr_parts.append(f"日辰({rizhen.name})が{target_wx.value}を剋ぁEↁE日剋（最凶�E�、E)
        elif is_ru_mu(target_wx, rizhen):
            curr_parts.append(f"日辰({rizhen.name})が{target_wx.value}の墁EↁE日墓（即時危機）、E)

        # 日月同辰チェチE���E�種本の強調事頁E��E
        if yuejian == rizhen:
            curr_parts.append(
                f"☁E��月同辰�E�Eyuejian.name}�E�：エネルギーが極端化、E
                + ("極旺、E if generates_target(yuejian) or same_wx(yuejian) else "絶地、E)
            )

        current_status = " ".join(curr_parts) if curr_parts else "月日ともに中立（平�E�、E

        best_names  = [d.name for d in best]
        worst_names = [d.name for d in worst]
        desc = (
            f"【{target_wx.value}爻の応期】\n"
            f"  吉応期�E�生じる・比和の地支�E�E {', '.join(best_names)}\n"
            f"  凶応期�E�剋す�E墓�E絶の地支�E�E {', '.join(worst_names)}\n"
            f"  現状: {current_status}"
        )

        return YingQiResult(
            target_wx=target_wx,
            best_dizhi=best,
            worst_dizhi=worst,
            current_status=current_status,
            description=desc,
        )


# ─────────────────────────────────────────────
# 入墓�E死絶 診断モジュール�E�EuMuDiagnostic�E�E
# ─────────────────────────────────────────────

@dataclass
class RuMuDiagnosticResult:
    """用神�E入墓�E死絶状態診断"""
    yao_pos:     int
    yao_wx:      GoXing
    ru_mu_yue:   bool   # 月建が墓地
    ru_mu_ri:    bool   # 日辰が墓地
    jue_di_yue:  bool   # 月建が絶地
    jue_di_ri:   bool   # 日辰が絶地
    si_di_yue:   bool   # 月建が死地
    si_di_ri:    bool   # 日辰が死地
    severity:    int    # 0、E�E�高いほど危機的�E�E
    prognosis:   str    # "救済可能" / "時間のみが解決" / "絶望的"
    description: str


class RuMuDiagnostic:
    """
    種本の根本思想 6�E�E
    「�E墓」「死絶」�E時間による救済不可能を示す、E
    救神（相生�E五行）が卦冁E��存在しなければ医療行為も無効、E
    """

    @staticmethod
    def diagnose(
        yao_a: YaoAnalysis,
        yuejian: DiZhi,
        rizhen: DiZhi,
        analyses: list[YaoAnalysis],
    ) -> RuMuDiagnosticResult:
        wx = yao_a.yao.wuxing
        pos = yao_a.yao.position

        ru_mu_yue  = is_ru_mu(wx, yuejian)
        ru_mu_ri   = is_ru_mu(wx, rizhen)
        jue_yue    = is_jue_di(wx, yuejian)
        jue_ri     = is_jue_di(wx, rizhen)
        si_yue     = is_si_di(wx, yuejian)
        si_ri      = is_si_di(wx, rizhen)

        severity = sum([ru_mu_yue, ru_mu_ri, jue_yue, jue_ri, si_yue, si_ri])

        # 救神�E存在確認（卦冁E��用神を生ずる五行�E爻があるか�E�E
        kyushin_exists = any(
            EnergyAnalyzer._sheng(a.yao.wuxing, wx) and not a.is_po
            for a in analyses
            if a.yao.position != pos
        )

        if severity == 0:
            prognosis = "救済可能"
        elif severity <= 2 and kyushin_exists:
            prognosis = "救済可能"
        elif severity <= 2:
            prognosis = "時間のみが解決"
        elif severity >= 3 and not kyushin_exists:
            prognosis = "絶望的"
        else:
            prognosis = "時間のみが解決"

        parts = [f"{pos}爻({wx.value}) の入墓�E死絶診断: "]
        flags = []
        if ru_mu_yue: flags.append(f"月墁E{yuejian.name})")
        if ru_mu_ri:  flags.append(f"日墁E{rizhen.name})")
        if jue_yue:   flags.append(f"月絶({yuejian.name})")
        if jue_ri:    flags.append(f"日絶({rizhen.name})")
        if si_yue:    flags.append(f"月死({yuejian.name})")
        if si_ri:     flags.append(f"日死({rizhen.name})")
        parts.append(", ".join(flags) if flags else "該当なぁE)
        parts.append(f" | 重篤度={severity} | 救祁E{'あり' if kyushin_exists else 'なぁE} | 予征E{prognosis}")

        return RuMuDiagnosticResult(
            yao_pos=pos, yao_wx=wx,
            ru_mu_yue=ru_mu_yue, ru_mu_ri=ru_mu_ri,
            jue_di_yue=jue_yue, jue_di_ri=jue_ri,
            si_di_yue=si_yue, si_di_ri=si_ri,
            severity=severity,
            prognosis=prognosis,
            description="".join(parts),
        )


# ─────────────────────────────────────────────
# Phase2 統合エンジン�E�EullDivinationEngine�E�E
# ─────────────────────────────────────────────

@dataclass
class FullDivinationResult:
    """Phase2を含む完�E占断結果"""
    base:            DivinationResult
    bian_yao:        list[BianYaoAnalysis]
    hui_tou_sheng:   list[HuiTouShengResult]
    homicide:        Optional[HomicideJudgment]
    ying_qi:         YingQiResult
    ru_mu:           Optional[RuMuDiagnosticResult]
    fu_shen:         Optional[FuShenResult]
    full_detail:     str


class FullDivinationEngine:

    def __init__(
        self,
        ctx: DivinationContext,
        qtype: QuestionType,
        gong: str = "乾",
        check_homicide: bool = False,
    ):
        self.ctx            = ctx
        self.qtype          = qtype
        self.gong           = gong
        self.check_homicide = check_homicide

    def run(self) -> FullDivinationResult:
        # Phase1 実衁E
        base_engine = DivinationEngine(self.ctx, self.qtype)
        base        = base_engine.run()
        analyses    = base.yao_analyses

        # 変爻・進退祁E
        bian_yao = BianYaoAnalyzer.analyze_all(self.ctx)

        # 回頭の生（用神位置を対象�E�E
        hui_tou = HuiTouShengDetector.detect(
            self.ctx, analyses, base.yong_shen_pos
        )

        # 他殺判定（フラグ有りの場合�Eみ�E�E
        homicide = None
        if self.check_homicide:
            homicide = HomicideJudgmentGateway.judge(analyses)

        # 用神�E五行で応期計箁E
        yong_a   = next(a for a in analyses if a.yao.position == base.yong_shen_pos)
        ying_qi  = YingQiCalculator.calc(yong_a.yao.wuxing, self.ctx.yuejian, self.ctx.rizhen)

        # 用神�E入墓�E死絶診断
        ru_mu = RuMuDiagnostic.diagnose(yong_a, self.ctx.yuejian, self.ctx.rizhen, analyses)

        # 伏神（用神が表卦に不在の場合！E
        mapping  = TargetGodMapper.get_mapping(self.qtype)
        fu_shen  = FuShenAnalyzer.find(self.ctx, mapping.yong_shen, self.gong)

        # フル詳細チE��スト生戁E
        parts = [
            "╁E * 60,
            f"  完�E占断レポ�EチE({self.qtype.value})",
            "╁E * 60,
            base.detail,
        ]
        if bian_yao:
            parts += ["", "─ 変爻・進退祁E─"]
            parts += [f"  {b.description}" for b in bian_yao]
        if hui_tou:
            parts += ["", "─ 回頭の甁E─"]
            parts += [f"  ☁E{h.description}" for h in hui_tou]
        if homicide:
            parts += ["", "─ 他殺判宁E─", f"  [{homicide.confidence}] {homicide.verdict}",
                      f"  {homicide.description}"]
        parts += ["", "─ 応期 ─", ying_qi.description]
        parts += ["", "─ 入墓�E死絶診断 ─", f"  {ru_mu.description}"]
        if fu_shen:
            parts += ["", "─ 伏祁E─", f"  {fu_shen.description}"]

        return FullDivinationResult(
            base=base,
            bian_yao=bian_yao,
            hui_tou_sheng=hui_tou,
            homicide=homicide,
            ying_qi=ying_qi,
            ru_mu=ru_mu,
            fu_shen=fu_shen,
            full_detail="\n".join(parts),
        )


# ─────────────────────────────────────────────
# Phase2 チE��トスイーチE
# ─────────────────────────────────────────────

class TestHuiTouSheng(unittest.TestCase):

    def test_basic_hui_tou_sheng(self):
        """火動爻→土化�E→土生��(用祁E = 回頭の甁E""
        # 世爻(用祁E=釁E申)。動爻=火(十Eが土(丁Eに化�E。土生�� ↁE回頭の甁E
        ctx = DivinationContext(
            yao_list=[
                Yao(1, LiuQin.GUAN_GUI, DiZhi.SHEN, YaoState.STATIC),
                Yao(2, LiuQin.FU_MU,   DiZhi.WU,   YaoState.DYNAMIC, DiZhi.CHOU),  # 火→土
                Yao(3, LiuQin.ZI_SUN,  DiZhi.MAO,  YaoState.STATIC),
                Yao(4, LiuQin.QI_CAI,  DiZhi.ZI,   YaoState.STATIC),
                Yao(5, LiuQin.XIONG_DI,DiZhi.YIN,  YaoState.STATIC),
                Yao(6, LiuQin.FU_MU,   DiZhi.HAI,  YaoState.STATIC),
            ],
            yuejian=DiZhi.ZI, rizhen=DiZhi.CHEN,
            shi_yao=1, ying_yao=4,
        )
        analyses = [EnergyAnalyzer.analyze(y, ctx.yuejian, ctx.rizhen) for y in ctx.yao_list]
        results = HuiTouShengDetector.detect(ctx, analyses, target_pos=1)
        self.assertTrue(len(results) > 0)
        r = results[0]
        self.assertEqual(r.hua_chu_wx, GoXing.EARTH)  # 丁E圁E
        self.assertTrue(r.detected)

    def test_no_hui_tou_sheng_when_no_dynamic(self):
        """動爻なぁEↁE回頭の生なぁE""
        ctx = DivinationContext(
            yao_list=[
                Yao(i, LiuQin.GUAN_GUI, DiZhi.SHEN, YaoState.STATIC)
                for i in range(1, 7)
            ],
            yuejian=DiZhi.ZI, rizhen=DiZhi.CHEN,
            shi_yao=1, ying_yao=4,
        )
        analyses = [EnergyAnalyzer.analyze(y, ctx.yuejian, ctx.rizhen) for y in ctx.yao_list]
        results = HuiTouShengDetector.detect(ctx, analyses, target_pos=1)
        self.assertEqual(results, [])

    def test_true_hui_tou_sheng_ke_then_sheng(self):
        """允E��剋する動爻が化出後に生ずめEↁE真�E回頭の生フラグ"""
        # 釁E勁E→水(化�E)→水生木(用祁E。��剋木だが化出後�E生、E
        ctx = DivinationContext(
            yao_list=[
                Yao(1, LiuQin.ZI_SUN,   DiZhi.YIN,  YaoState.STATIC),   # 木(用祁E
                Yao(2, LiuQin.GUAN_GUI,  DiZhi.SHEN, YaoState.DYNAMIC, DiZhi.ZI),  # 金�E水
                Yao(3, LiuQin.QI_CAI,   DiZhi.MAO,  YaoState.STATIC),
                Yao(4, LiuQin.XIONG_DI, DiZhi.WU,   YaoState.STATIC),
                Yao(5, LiuQin.FU_MU,    DiZhi.CHEN, YaoState.STATIC),
                Yao(6, LiuQin.ZI_SUN,   DiZhi.HAI,  YaoState.STATIC),
            ],
            yuejian=DiZhi.ZI, rizhen=DiZhi.CHEN,
            shi_yao=1, ying_yao=4,
        )
        analyses = [EnergyAnalyzer.analyze(y, ctx.yuejian, ctx.rizhen) for y in ctx.yao_list]
        results = HuiTouShengDetector.detect(ctx, analyses, target_pos=1)
        self.assertTrue(any(r.detected for r in results))
        # 真�E回頭�E�剋→生�E��E記述を確誁E
        self.assertTrue(any("真�E回頭" in r.description for r in results))


class TestBianYaoAnalyzer(unittest.TestCase):

    def test_jin_shen(self):
        """孁E水)→亥(水)は退神、寁E木)→卯(木)は進祁E""
        ctx = DivinationContext(
            yao_list=[
                Yao(1, LiuQin.XIONG_DI, DiZhi.ZI,  YaoState.DYNAMIC, DiZhi.HAI),  # 水退
                Yao(2, LiuQin.ZI_SUN,   DiZhi.YIN, YaoState.DYNAMIC, DiZhi.MAO),  # 木進
                Yao(3, LiuQin.QI_CAI,   DiZhi.WU,  YaoState.STATIC),
                Yao(4, LiuQin.GUAN_GUI, DiZhi.YOU, YaoState.STATIC),
                Yao(5, LiuQin.FU_MU,    DiZhi.WEI, YaoState.STATIC),
                Yao(6, LiuQin.XIONG_DI, DiZhi.SI,  YaoState.STATIC),
            ],
            yuejian=DiZhi.ZI, rizhen=DiZhi.CHEN,
            shi_yao=1, ying_yao=4,
        )
        results = BianYaoAnalyzer.analyze_all(ctx)
        self.assertEqual(len(results), 2)
        tui = next(r for r in results if r.yao_pos == 1)
        jin = next(r for r in results if r.yao_pos == 2)
        self.assertTrue(tui.is_tui)
        self.assertFalse(tui.is_jin)
        self.assertTrue(jin.is_jin)
        self.assertFalse(jin.is_tui)

    def test_ru_mu_bian(self):
        """木(寁E動爻が未(木の墁Eに化�E ↁEru_mu_bian=True"""
        ctx = DivinationContext(
            yao_list=[
                Yao(1, LiuQin.ZI_SUN, DiZhi.YIN, YaoState.DYNAMIC, DiZhi.WEI),  # 木→未�E�木の墓！E
                Yao(2, LiuQin.GUAN_GUI, DiZhi.WU,  YaoState.STATIC),
                Yao(3, LiuQin.QI_CAI,   DiZhi.YOU, YaoState.STATIC),
                Yao(4, LiuQin.XIONG_DI, DiZhi.ZI,  YaoState.STATIC),
                Yao(5, LiuQin.FU_MU,    DiZhi.HAI, YaoState.STATIC),
                Yao(6, LiuQin.ZI_SUN,   DiZhi.MAO, YaoState.STATIC),
            ],
            yuejian=DiZhi.ZI, rizhen=DiZhi.CHEN,
            shi_yao=1, ying_yao=4,
        )
        results = BianYaoAnalyzer.analyze_all(ctx)
        self.assertEqual(len(results), 1)
        self.assertTrue(results[0].ru_mu_bian)


class TestHomicideJudgment(unittest.TestCase):

    def test_static_guan_is_natural_death(self):
        """官鬼が静爻 ↁE痁E��・事故 確宁E""
        yao_list = [
            Yao(1, LiuQin.ZI_SUN,    DiZhi.ZI,  YaoState.STATIC),
            Yao(2, LiuQin.GUAN_GUI,  DiZhi.YIN, YaoState.STATIC),  # 静爻
            Yao(3, LiuQin.QI_CAI,    DiZhi.MAO, YaoState.STATIC),
            Yao(4, LiuQin.XIONG_DI,  DiZhi.SI,  YaoState.STATIC),
            Yao(5, LiuQin.FU_MU,     DiZhi.WEI, YaoState.STATIC),
            Yao(6, LiuQin.ZI_SUN,    DiZhi.YOU, YaoState.STATIC),
        ]
        analyses = [EnergyAnalyzer.analyze(y, DiZhi.ZI, DiZhi.CHEN) for y in yao_list]
        j = HomicideJudgmentGateway.judge(analyses)
        self.assertEqual(j.verdict, "痁E��・事故")
        self.assertEqual(j.confidence, "確宁E)
        self.assertFalse(j.guan_is_dynamic)

    def test_dynamic_strong_guan_is_suspicious(self):
        """官鬼が旺相動爻 ↁE他殺疑い 有力"""
        yao_list = [
            Yao(1, LiuQin.ZI_SUN,   DiZhi.ZI,  YaoState.STATIC),
            Yao(2, LiuQin.GUAN_GUI, DiZhi.YIN, YaoState.DYNAMIC),  # 動爻・子月→相
            Yao(3, LiuQin.QI_CAI,   DiZhi.MAO, YaoState.STATIC),
            Yao(4, LiuQin.XIONG_DI, DiZhi.SI,  YaoState.STATIC),
            Yao(5, LiuQin.FU_MU,    DiZhi.WEI, YaoState.STATIC),
            Yao(6, LiuQin.ZI_SUN,   DiZhi.YOU, YaoState.STATIC),
        ]
        analyses = [EnergyAnalyzer.analyze(y, DiZhi.ZI, DiZhi.CHEN) for y in yao_list]
        j = HomicideJudgmentGateway.judge(analyses)
        self.assertEqual(j.verdict, "他殺疑い")
        self.assertTrue(j.guan_is_dynamic)

    def test_broken_dynamic_guan_is_accident(self):
        """官鬼が動爻だが月破 ↁE痁E��・事故"""
        yao_list = [
            Yao(1, LiuQin.ZI_SUN,   DiZhi.ZI,  YaoState.STATIC),
            Yao(2, LiuQin.GUAN_GUI, DiZhi.WU,  YaoState.DYNAMIC),  # 子月→月破
            Yao(3, LiuQin.QI_CAI,   DiZhi.MAO, YaoState.STATIC),
            Yao(4, LiuQin.XIONG_DI, DiZhi.SI,  YaoState.STATIC),
            Yao(5, LiuQin.FU_MU,    DiZhi.WEI, YaoState.STATIC),
            Yao(6, LiuQin.ZI_SUN,   DiZhi.YOU, YaoState.STATIC),
        ]
        analyses = [EnergyAnalyzer.analyze(y, DiZhi.ZI, DiZhi.CHEN) for y in yao_list]
        j = HomicideJudgmentGateway.judge(analyses)
        self.assertEqual(j.verdict, "痁E��・事故")
        self.assertTrue(j.guan_is_broken)


class TestYingQiCalculator(unittest.TestCase):

    def test_metal_best_and_worst(self):
        """金�E吉応期�E�土・金）と凶応期�E�火・木の墓！E""
        r = YingQiCalculator.calc(GoXing.METAL, DiZhi.ZI, DiZhi.CHEN)
        # 土が金を生ず ↁE吁E
        earth_dz = [d for d in r.best_dizhi if wuxing_of(d) == GoXing.EARTH]
        self.assertTrue(len(earth_dz) > 0)
        # 火が��を剋ぁEↁE凶
        fire_dz = [d for d in r.worst_dizhi if wuxing_of(d) == GoXing.FIRE]
        self.assertTrue(len(fire_dz) > 0)

    def test_nichi_getsu_same(self):
        """日月同辰 ↁE極端化フラグが説明文に含まれる"""
        r = YingQiCalculator.calc(GoXing.WATER, DiZhi.ZI, DiZhi.ZI)
        self.assertIn("日月同辰", r.current_status)

    def test_nichi_getsu_kill(self):
        """月建が用神を剋す ↁE月剋の説昁E""
        # 釁E申朁Eが木を剋ぁE
        r = YingQiCalculator.calc(GoXing.WOOD, DiZhi.SHEN, DiZhi.CHEN)
        self.assertIn("月剋", r.current_status)


class TestRuMuDiagnostic(unittest.TestCase):

    def test_diana_double_mu(self):
        """ダイアナ妁E��ース�E��E月�E日に金爻 ↁE二重入墁E""
        # 酁E釁E爻、月建=戌、日辰=戌（��の墁E丑�Eはずだが種本は戌を金�E墓とも論ずる！E
        # ここでは種本準拠で金�E墁E丑。ただし�Eは火の墓（土�E�で金を囲む象、E
        # チE��ト：��(YOU)爻が丑月丑日に ↁE二重入墁E
        yao_list = [
            Yao(1, LiuQin.GUAN_GUI, DiZhi.YOU, YaoState.STATIC),
            Yao(2, LiuQin.ZI_SUN,   DiZhi.YIN, YaoState.STATIC),
            Yao(3, LiuQin.QI_CAI,   DiZhi.MAO, YaoState.STATIC),
            Yao(4, LiuQin.XIONG_DI, DiZhi.WU,  YaoState.STATIC),
            Yao(5, LiuQin.FU_MU,    DiZhi.WEI, YaoState.STATIC),
            Yao(6, LiuQin.ZI_SUN,   DiZhi.HAI, YaoState.STATIC),
        ]
        analyses = [EnergyAnalyzer.analyze(y, DiZhi.CHOU, DiZhi.CHOU) for y in yao_list]
        yao_a = analyses[0]  # 金爻
        result = RuMuDiagnostic.diagnose(yao_a, DiZhi.CHOU, DiZhi.CHOU, analyses)
        self.assertTrue(result.ru_mu_yue)
        self.assertTrue(result.ru_mu_ri)
        self.assertGreaterEqual(result.severity, 2)

    def test_no_crisis(self):
        """入墓�E死絶なぁEↁE重篤度0"""
        yao_list = [Yao(1, LiuQin.ZI_SUN, DiZhi.YIN, YaoState.STATIC)]
        analyses = [EnergyAnalyzer.analyze(y, DiZhi.ZI, DiZhi.CHEN) for y in yao_list]
        result = RuMuDiagnostic.diagnose(analyses[0], DiZhi.ZI, DiZhi.CHEN, analyses)
        self.assertEqual(result.severity, 0)


class TestFuShenAnalyzer(unittest.TestCase):

    def test_fu_shen_detected_when_absent(self):
        """用神（妻財�E�が表卦に不在 ↁE伏神を返す"""
        # 表卦に QI_CAI なぁE
        yao_list = [
            Yao(1, LiuQin.XIONG_DI, DiZhi.ZI,  YaoState.STATIC),
            Yao(2, LiuQin.GUAN_GUI, DiZhi.YIN, YaoState.STATIC),
            Yao(3, LiuQin.ZI_SUN,  DiZhi.CHEN,YaoState.STATIC),
            Yao(4, LiuQin.FU_MU,   DiZhi.WU,  YaoState.STATIC),
            Yao(5, LiuQin.GUAN_GUI,DiZhi.SHEN,YaoState.STATIC),
            Yao(6, LiuQin.ZI_SUN,  DiZhi.XU,  YaoState.STATIC),
        ]
        ctx = DivinationContext(
            yao_list=yao_list,
            yuejian=DiZhi.ZI, rizhen=DiZhi.CHEN,
            shi_yao=1, ying_yao=4,
        )
        result = FuShenAnalyzer.find(ctx, LiuQin.QI_CAI, "乾")
        self.assertIsNotNone(result)

    def test_fu_shen_none_when_present(self):
        """用神が表卦に存在する ↁENone を返す"""
        yao_list = [
            Yao(1, LiuQin.QI_CAI,   DiZhi.ZI,  YaoState.STATIC),
            Yao(2, LiuQin.GUAN_GUI, DiZhi.YIN, YaoState.STATIC),
            Yao(3, LiuQin.ZI_SUN,  DiZhi.MAO, YaoState.STATIC),
            Yao(4, LiuQin.FU_MU,   DiZhi.SI,  YaoState.STATIC),
            Yao(5, LiuQin.XIONG_DI,DiZhi.WEI, YaoState.STATIC),
            Yao(6, LiuQin.ZI_SUN,  DiZhi.YOU, YaoState.STATIC),
        ]
        ctx = DivinationContext(
            yao_list=yao_list,
            yuejian=DiZhi.ZI, rizhen=DiZhi.CHEN,
            shi_yao=1, ying_yao=4,
        )
        result = FuShenAnalyzer.find(ctx, LiuQin.QI_CAI, "乾")
        self.assertIsNone(result)


class TestFullDivinationEngine(unittest.TestCase):

    def test_full_engine_with_hui_tou_sheng(self):
        """回頭の生を含む完�E占断が正常に実行される"""
        ctx = DivinationContext(
            yao_list=[
                Yao(1, LiuQin.GUAN_GUI, DiZhi.SHEN, YaoState.STATIC),   # 釁E用神�E仕亁E
                Yao(2, LiuQin.FU_MU,    DiZhi.WU,   YaoState.DYNAMIC, DiZhi.CHOU),  # 火→土(回頭の生候裁E
                Yao(3, LiuQin.ZI_SUN,   DiZhi.MAO,  YaoState.STATIC),
                Yao(4, LiuQin.QI_CAI,   DiZhi.ZI,   YaoState.STATIC),
                Yao(5, LiuQin.XIONG_DI, DiZhi.YIN,  YaoState.STATIC),
                Yao(6, LiuQin.FU_MU,    DiZhi.HAI,  YaoState.STATIC),
            ],
            yuejian=DiZhi.ZI, rizhen=DiZhi.CHEN,
            shi_yao=1, ying_yao=4,
        )
        engine = FullDivinationEngine(ctx, QuestionType.CAREER, gong="乾")
        result = engine.run()
        self.assertIsNotNone(result.base)
        self.assertTrue(len(result.bian_yao) > 0)
        # 回頭の生が検�Eされるか確認（火→土→土生�߁E�E
        self.assertTrue(len(result.hui_tou_sheng) > 0)

    def test_full_engine_homicide_check(self):
        """他殺判定付き完�E占断"""
        ctx = DivinationContext(
            yao_list=[
                Yao(1, LiuQin.ZI_SUN,   DiZhi.ZI,  YaoState.STATIC),
                Yao(2, LiuQin.GUAN_GUI, DiZhi.YIN, YaoState.STATIC),  # 静爻 ↁE他殺否宁E
                Yao(3, LiuQin.QI_CAI,   DiZhi.MAO, YaoState.STATIC),
                Yao(4, LiuQin.XIONG_DI, DiZhi.SI,  YaoState.STATIC),
                Yao(5, LiuQin.FU_MU,    DiZhi.WEI, YaoState.STATIC),
                Yao(6, LiuQin.ZI_SUN,   DiZhi.YOU, YaoState.STATIC),
            ],
            yuejian=DiZhi.ZI, rizhen=DiZhi.CHEN,
            shi_yao=1, ying_yao=4,
        )
        engine = FullDivinationEngine(
            ctx, QuestionType.HEALTH, gong="坁E, check_homicide=True
        )
        result = engine.run()
        self.assertIsNotNone(result.homicide)
        self.assertEqual(result.homicide.verdict, "痁E��・事故")
        self.assertEqual(result.homicide.confidence, "確宁E)
