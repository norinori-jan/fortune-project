from __future__ import annotations

from dataclasses import dataclass

from .hexagrams import HexagramResult


@dataclass(frozen=True)
class ReadingResult:
    """
    易経の解釈結果
    """

    # 卦情報
    hexagram_number: int
    hexagram_name: str

    # 卦辞
    judgement: dict

    # 象伝
    image: dict

    # 変爻
    changing_lines: list[dict]

    # 全爻
    yao: dict

    # キーワード
    keywords: list[str]

    # 要約
    summary: str

    # 助言
    advice: str


class InterpretationEngine:
    """
    易経の解釈エンジン

    HexagramEngine が生成した HexagramResult を
    人が読みやすい ReadingResult へ変換する。
    """

    # ---------------------------------------------------------
    # 解釈
    # ---------------------------------------------------------

    def interpret(
        self,
        result: HexagramResult,
    ) -> ReadingResult:

        changing = []

        keywords = []

        advice = []

        for line in result.changing_lines:

            data = (
                result.yao
                .get("lines", {})
                .get(str(line), {})
            )

            if data:

                changing.append(data)

                keywords.extend(
                    data.get(
                        "keywords",
                        [],
                    )
                )

                if data.get("advice"):

                    advice.append(
                        data["advice"]
                    )

        # 重複除去
        keywords = list(
            dict.fromkeys(keywords)
        )

        summary = (
            result.judgement.get(
                "meaning",
                "",
            )
            if result.judgement
            else ""
        )

        return ReadingResult(

            hexagram_number=result.hexagram_number,

            hexagram_name=result.hexagram_name,

            judgement=result.judgement,

            image=result.image,

            changing_lines=changing,

            yao=result.yao,

            keywords=keywords,

            summary=summary,

            advice="\n".join(advice),

        )

    # ---------------------------------------------------------
    # 卦辞のみ
    # ---------------------------------------------------------

    def get_judgement(
        self,
        result: HexagramResult,
    ) -> dict:

        return result.judgement

    # ---------------------------------------------------------
    # 象伝のみ
    # ---------------------------------------------------------

    def get_image(
        self,
        result: HexagramResult,
    ) -> dict:

        return result.image

    # ---------------------------------------------------------
    # 変爻のみ
    # ---------------------------------------------------------

    def get_changing_lines(
        self,
        result: HexagramResult,
    ) -> list[dict]:

        lines = []

        for line in result.changing_lines:

            data = (
                result.yao
                .get("lines", {})
                .get(str(line), {})
            )

            if data:

                lines.append(data)

        return lines

    # ---------------------------------------------------------
    # キーワード
    # ---------------------------------------------------------

    def get_keywords(
        self,
        result: HexagramResult,
    ) -> list[str]:

        keywords = []

        for line in result.changing_lines:

            data = (
                result.yao
                .get("lines", {})
                .get(str(line), {})
            )

            keywords.extend(
                data.get(
                    "keywords",
                    [],
                )
            )

        return list(
            dict.fromkeys(keywords)
        )

    # ---------------------------------------------------------
    # アドバイス
    # ---------------------------------------------------------

    def get_advice(
        self,
        result: HexagramResult,
    ) -> str:

        advice = []

        for line in result.changing_lines:

            data = (
                result.yao
                .get("lines", {})
                .get(str(line), {})
            )

            if data.get("advice"):

                advice.append(
                    data["advice"]
                )

        return "\n".join(advice)