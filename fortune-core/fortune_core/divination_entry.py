"""
divination_entry.py
====================

占ぁE�E入り口�E�ユーザーの相諁E�E容をヒアリングして、E
最適な占術（タロチE��・風水・褁E��占法）を自動判定�E提案するモジュール、E

主要機�E:
- 相諁E�E容の刁E��（恋愛、仕事、E��運、人間関係、健康など�E�E
- キーワード�E析から最適な占術を推薦
- ユーザーに対する提案文の生�E
"""

import json
from dataclasses import dataclass
from typing import Literal
from datetime import datetime


# ---------------------------------------------------------------------------
# 定数定義
# ---------------------------------------------------------------------------

DivationType = Literal["tarot_celtic_cross", "feng_shui", "four_pillars", "combined"]
ConcernType = Literal["love", "work", "money", "relationship", "health", "future", "general"]

# 相諁E��チE��リのキーワード�EチE��ング
CONCERN_KEYWORDS: dict[ConcernType, list[str]] = {
    "love": [
        "恋�E", "彼氁E, "彼女", "パ�Eトナー", "結婁E, "婚活", "牁E��い",
        "恁E, "チE�EチE, "告白", "好ぁE, "愁E, "愛情", "交隁E, "関俁E,
        "love", "romantic", "boyfriend", "girlfriend", "marriage",
    ],
    "work": [
        "仕亁E, "転職", "職場", "上司", "同�E", "プロジェクチE, "キャリア",
        "昁E��", "退職", "失業", "起業", "独竁E, "キャリアパス",
        "work", "job", "career", "employment", "boss", "promotion",
    ],
    "money": [
        "金運", "お��", "給斁E, "年叁E, "投賁E, "株", "ビジネス", "啁E��",
        "貯釁E, "借��", "返渁E, "経営", "利盁E, "収�E", "支出",
        "money", "financial", "investment", "income", "business",
    ],
    "relationship": [
        "人間関俁E, "友人", "家旁E, "親", "允E��E, "姉妹", "友達", "知人",
        "人付き合い", "対人", "信頼", "葛藤", "和解", "別めE,
        "relationship", "friend", "family", "parent",
    ],
    "health": [
        "健康", "痁E��E, "体調", "治癁E, "痁E��", "医師", "診断", "回復",
        "ストレス", "睡眠", "運動", "食亁E, "メンタル", "忁E��",
        "health", "medical", "illness", "treatment", "wellness",
    ],
    "future": [
        "未来", "前�E", "予測", "予感", "チャンス", "運命", "天命",
        "タイミング", "可能性", "展開", "封E��", "次", "後、E,
        "future", "destiny", "fortune", "prediction", "outcome",
    ],
}

# タロチE��が推奨される悩みの特徴
TAROT_OPTIMIZED_KEYWORDS: list[str] = [
    "仁E, "近未来", "3ヶ朁E, "半年", "今征E, "進め方", "決断",
    "どぁE��べぁE, "どぁE��めE, "今後�E方吁E, "状況E, "対忁E,
    "展開", "流れ", "進むべぁE, "今�E状況E, "こ�E允E,
    "soon", "near future", "how should", "what should",
]

# 東洋占術が推奨される悩みの特徴
FENG_SHUI_OPTIMIZED_KEYWORDS: list[str] = [
    "根本", "本質", "適職", "天職", "才�E", "賁E��", "引っ越し", "方佁E,
    "環墁E, "運氁E, "気�E流れ", "エネルギー", "バイオリズム", "周朁E,
    "宿命", "宿昁E, "本来の", "真�E", "長朁E, "長年", "根強ぁE,
    "essence", "talent", "relocation", "long-term", "fundamental",
]

# 褁E��占法が推奨される悩みの特徴
COMBINED_OPTIMIZED_KEYWORDS: list[str] = [
    "褁E��", "褁E��", "総合", "全体的", "人甁E, "人生設訁E, "多角的",
    "匁E��皁E, "統吁E, "全方佁E, "シナリオ", "選択肢", "比輁E,
]

# ---------------------------------------------------------------------------
# チE�Eタクラス
# ---------------------------------------------------------------------------


@dataclass
class DivineRecommendation:
    """占術推奨結果"""
    divination_type: DivationType
    confidence: float  # 0.0 ~ 1.0
    concern_category: ConcernType
    reasoning: str
    user_guidance: str
    keywords_matched: list[str]

    def to_dict(self) -> dict:
        """JSON シリアライズ用"""
        return {
            "divination_type": self.divination_type,
            "confidence": self.confidence,
            "concern_category": self.concern_category,
            "reasoning": self.reasoning,
            "user_guidance": self.user_guidance,
            "keywords_matched": self.keywords_matched,
        }


@dataclass
class DivineEntry:
    """占ぁE��チE��ョン開始データ"""
    query_text: str
    query_text_ja: str
    concern_type: ConcernType
    recommendation: DivineRecommendation
    session_id: str
    created_at: str

    def to_dict(self) -> dict:
        """JSON シリアライズ用"""
        return {
            "query_text": self.query_text,
            "query_text_ja": self.query_text_ja,
            "concern_type": self.concern_type,
            "recommendation": self.recommendation.to_dict(),
            "session_id": self.session_id,
            "created_at": self.created_at,
        }


# ---------------------------------------------------------------------------
# 占術推奨エンジン
# ---------------------------------------------------------------------------


class DivineEntryEngine:
    """
    ユーザーの相諁E�E容をヒアリングして、最適な占術を推奨するエンジン、E
    """

    def __init__(self):
        """初期匁E""
        pass

    def _extract_concern_type(self, query: str) -> tuple[ConcernType, float]:
        """
        相諁E�E容からカチE��リを推定（スコア付き�E�、E
        褁E��該当する場合�E最も確度が高いも�Eを返す、E

        Returns:
            (concern_type, confidence) - タイプと確度�E�E.0�E�E.0�E�E
        """
        query_lower = query.lower()
        concern_scores: dict[ConcernType, float] = {t: 0.0 for t in [
            "love", "work", "money", "relationship", "health", "future", "general"
        ]}

        for concern_type, keywords in CONCERN_KEYWORDS.items():
            for keyword in keywords:
                if keyword.lower() in query_lower:
                    concern_scores[concern_type] += 1.0

        # 正規化
        max_score = max(concern_scores.values())
        if max_score > 0:
            concern_scores = {k: v / max_score for k, v in concern_scores.items()}

        # スコアが最も高いカチE��リを選抁E
        best_concern = max(concern_scores, key=concern_scores.get)
        confidence = concern_scores[best_concern]

        return best_concern, confidence

    def _recommend_divination_type(self, query: str, concern: ConcernType) -> DivineRecommendation:
        """
        相諁E�E容から最適な占術を推奨する、E
        """
        query_lower = query.lower()

        # 吁E��術�E符号度をスコアリング
        tarot_score = 0.0
        feng_shui_score = 0.0
        combined_score = 0.0

        # タロチE��が推奨される特徴をスコアリング
        for keyword in TAROT_OPTIMIZED_KEYWORDS:
            if keyword.lower() in query_lower:
                tarot_score += 1.5

        # 東洋占術が推奨される特徴をスコアリング
        for keyword in FENG_SHUI_OPTIMIZED_KEYWORDS:
            if keyword.lower() in query_lower:
                feng_shui_score += 1.5

        # 褁E��占法が推奨される特徴をスコアリング
        for keyword in COMBINED_OPTIMIZED_KEYWORDS:
            if keyword.lower() in query_lower:
                combined_score += 1.5

        # 相諁E��チE��リによるボ�Eナス
        if concern in ["love", "future"]:
            tarot_score += 2.0
        elif concern in ["work", "money"]:
            tarot_score += 1.5
            feng_shui_score += 1.0

        if concern in ["work", "money", "health"]:
            feng_shui_score += 2.0

        if concern == "general":
            combined_score += 1.0

        # 正規化
        total_score = tarot_score + feng_shui_score + combined_score
        if total_score == 0:
            tarot_score = 1.0
            total_score = 1.0

        tarot_confidence = tarot_score / total_score
        feng_shui_confidence = feng_shui_score / total_score
        combined_confidence = combined_score / total_score

        # 推奨タイプ決宁E
        scores = {
            "tarot_celtic_cross": tarot_confidence,
            "feng_shui": feng_shui_confidence,
            "combined": combined_confidence,
        }
        recommended_type: DivationType = max(scores, key=scores.get)  # type: ignore

        # 推奨斁E��生�E
        guidance_map: dict[DivationType, str] = {
            "tarot_celtic_cross": (
                "あなた�Eそ�Eお悩みには、状況�E深層忁E��と未来の展開めE0本の柱で解き�Eかす"
                "【タロチE��・ケルト十字スプレチE��】が最も適してぁE��す、En"
                "今この瞬間�E忁E��状態から、E�E�Eヶ月�Eの展開まで、詳細に読み解きます、En"
                "それでは、シャチE��ルへ進みましょぁE��…"
            ),
            "feng_shui": (
                "あなた�Eそ�Eお悩みには、あなた�E根本皁E��賁E��と運気�E周期を読み解ぁE
                "【東洋占術�E風水�E�E��柱推命褁E��診断】が最も適してぁE��す、En"
                "長期的なバイオリズムと環墁E��ネルギーから、人生�E本質皁E��流れを�Eかします、En"
                "それでは、あなた�E生年月日と現在地をお聞かせください……"
            ),
            "combined": (
                "あなた�Eそ�Eお悩みには、短期�E忁E��皁E��開と長期�E宿命皁E��イオリズムめE
                "【褁E��占法】で総合皁E��読み解くことが最も適してぁE��す、En"
                "タロチE��と東洋占術�E両面からアプローチし、E60度からの視点を提供します、En"
                "それでは、シャチE��ルと四柱推命の準備を進めてぁE��ましょぁE��…"
            ),
        }

        reasoning_map: dict[DivationType, str] = {
            "tarot_celtic_cross": (
                f"相諁E�E容に「{', '.join(TAROT_OPTIMIZED_KEYWORDS[:3])}」などの"
                "近期皁E�E具体的なキーワードが含まれており、E
                "タロチE��の即座の忁E��読解が最適です、E
            ),
            "feng_shui": (
                f"相諁E�E容に「{', '.join(FENG_SHUI_OPTIMIZED_KEYWORDS[:3])}」などの"
                "根本皁E�E長期的なキーワードが含まれており、E
                "東洋占術�E本質皁E�E運命皁E��解が最適です、E
            ),
            "combined": (
                "褁E��の異なる�E面からの総合皁E��判断が忁E��な相諁E�E容です、E
                "短期と長期、忁E��と運命の両面から匁E��皁E��診断します、E
            ),
        }

        return DivineRecommendation(
            divination_type=recommended_type,
            confidence=scores[recommended_type],
            concern_category=concern,
            reasoning=reasoning_map[recommended_type],
            user_guidance=guidance_map[recommended_type],
            keywords_matched=[
                kw for kw in TAROT_OPTIMIZED_KEYWORDS + FENG_SHUI_OPTIMIZED_KEYWORDS + COMBINED_OPTIMIZED_KEYWORDS
                if kw.lower() in query_lower
            ][:5],
        )

    def create_entry(self, query_text: str, query_text_ja: str = "") -> DivineEntry:
        """
        新規占ぁE��チE��ョンを開始し、推奨占術を返す、E

        Parameters
        ----------
        query_text : str
            ユーザーの相諁E�E容�E�日本誁Eor 英語！E
        query_text_ja : str
            相諁E�E容の日本語！Euery_text が英語�E場合に持E��！E

        Returns
        -------
        DivineEntry
            占ぁE��チE��ョン開始データ
        """
        # 相諁E��チE��リを推宁E
        concern_type, _ = self._extract_concern_type(query_text)

        # 最適な占術を推奨
        recommendation = self._recommend_divination_type(query_text, concern_type)

        # セチE��ョンID生�E�E�タイムスタンチEベ�Eス�E�E
        now = datetime.now()
        session_id = f"divine_{int(now.timestamp() * 1000)}"

        entry = DivineEntry(
            query_text=query_text,
            query_text_ja=query_text_ja,
            concern_type=concern_type,
            recommendation=recommendation,
            session_id=session_id,
            created_at=now.isoformat(),
        )

        return entry

    def suggest_follow_up_questions(self, entry: DivineEntry) -> list[str]:
        """
        推奨占術に基づぁE��、ユーザーへのフォローアチE�E質問を生�E、E
        """
        questions_by_type: dict[DivationType, list[str]] = {
            "tarot_celtic_cross": [
                "こ�E相諁E��つぁE��もう少し詳しく教えてぁE��だけますか�E�E
                "�E�例：期限、E��係老E��現在のアクション�E�E,
                "こ�E相諁E��対して、あなたが一番知りたぁE��とは何ですか�E�E,
                "シャチE��ルを始める前に、この相諁E��を忁E��思い浮かべながら"
                "ストップ�Eタンを押してください。あなた�E直感がカードを選びます、E,
            ],
            "feng_shui": [
                "あなた�E生年月日をお聞かせください、E,
                "現在お住まぁE�E地域（できれば方位も�E�をお教えください、E,
                "こ�E問題でどのくらぁE�E期間お悩みですか�E�E,
            ],
            "combined": [
                "生年月日をお聞かせください、E,
                "こ�E相諁E�E期間軸は短期か長期か、あるいは両方ですか�E�E,
                "シャチE��ルと四柱推命の両チE�Eタを揃えて、総合診断を開始します、E,
            ],
        }

        return questions_by_type.get(entry.recommendation.divination_type, [])
