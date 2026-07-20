# fortune_core/iching/hexagrams.py

from __future__ import annotations

from dataclasses import dataclass

from .registry_loader import RegistryLoader


@dataclass(frozen=True)
class HexagramResult:
    """
    易経鑑定結果
    """

    # 入力された6本の爻（6,7,8,9）
    numbers: list[int]

    # 陰陽（0=陰、1=陽）
    yin_yang: list[int]

    # 下卦・上卦
    lower_trigram: str
    upper_trigram: str

    # 六十四卦
    hexagram_number: int
    hexagram_name: str

    # judgement.json
    judgement: dict

    # image.json
    image: dict

    # yao.json（1卦分）
    yao: dict

    # 変爻
    changing_lines: list[int]

    # -------------------------------
    # 変卦（之卦）
    # -------------------------------

    changed_hexagram_number: int

    changed_hexagram_name: str

    changed_judgement: dict

    changed_image: dict

    changed_yao: dict

class HexagramEngine:
    """
    易経エンジン

    RegistryLoader 経由で
        ・八卦
        ・六十四卦
        ・卦辞
        ・象伝
        ・爻辞
    を取得する。

    Engine は JSON の場所や構造を意識しない。
    """

    def __init__(self) -> None:

        self.registry = RegistryLoader()

        self.trigrams = self.registry.load_trigrams()
        self.hexagrams = self.registry.load_hexagrams()
        self.judgements = self.registry.load_judgements()
        self.images = self.registry.load_images()
        self.yao = self.registry.load_yao()

    # ---------------------------------------------------------
    # 八卦検索
    # ---------------------------------------------------------

    def _find_trigram(
        self,
        bits: tuple[int, int, int],
    ) -> str:

        for name, data in self.trigrams.items():

            if tuple(data["binary"]) == bits:
                return name

        raise ValueError(f"Unknown trigram: {bits}")

    # ---------------------------------------------------------
    # 六十四卦検索
    # ---------------------------------------------------------

    def _find_hexagram(
        self,
        upper: str,
        lower: str,
    ) -> dict | None:

        for item in self.hexagrams:

            if (
                item["upper"] == upper
                and item["lower"] == lower
            ):
                return item

        return None

    # ---------------------------------------------------------
    # 卦生成
    # ---------------------------------------------------------

    def generate(
        self,
        numbers: list[int],
    ) -> HexagramResult:

        if len(numbers) != 6:
            raise ValueError("6本の爻が必要です。")

        yin_yang = [
            1 if n % 2 else 0
            for n in numbers
        ]

        lower_bits = tuple(yin_yang[:3])
        upper_bits = tuple(yin_yang[3:])

        lower_name = self._find_trigram(lower_bits)
        upper_name = self._find_trigram(upper_bits)

        changing_lines = [
            i + 1
            for i, value in enumerate(numbers)
            if value in (6, 9)
        ]

        hexagram = self._find_hexagram(
            upper_name,
            lower_name,
        )

        if hexagram is None:

            return HexagramResult(
                numbers=numbers,
                yin_yang=yin_yang,
                lower_trigram=lower_name,
                upper_trigram=upper_name,
                hexagram_number=0,
                hexagram_name="未登録",
                judgement={},
                image={},
                yao={},
                changing_lines=changing_lines,

                changed_hexagram_number=0,
                changed_hexagram_name="",
                changed_judgement={},
                changed_image={},
                changed_yao={},
            )

        number = hexagram["number"]

        # 本卦（仮）
        current = HexagramResult(
            numbers=numbers,
            yin_yang=yin_yang,
            lower_trigram=lower_name,
            upper_trigram=upper_name,
            hexagram_number=number,
            hexagram_name=hexagram["name"],
            judgement=self.judgements.get(
                str(number),
                {},
            ),
            image=self.images.get(
                str(number),
                {},
            ),
            yao=self.yao.get(
                str(number),
                {},
            ),
            changing_lines=changing_lines,

            changed_hexagram_number=0,
            changed_hexagram_name="",
            changed_judgement={},
            changed_image={},
            changed_yao={},
        )

        changed = self.get_changed_hexagram(current)

        return HexagramResult(
            numbers=numbers,
            yin_yang=yin_yang,
            lower_trigram=lower_name,
            upper_trigram=upper_name,
            hexagram_number=number,
            hexagram_name=hexagram["name"],
            judgement=self.judgements.get(
                str(number),
                {},
            ),
            image=self.images.get(
                str(number),
                {},
            ),
            yao=self.yao.get(
                str(number),
                {},
            ),
            changing_lines=changing_lines,

            changed_hexagram_number=changed.get(
                "number",
                0,
            ),
            changed_hexagram_name=changed.get(
                "name",
                "",
            ),
            changed_judgement=changed.get(
                "judgement",
                {},
            ),
            changed_image=changed.get(
                "image",
                {},
            ),
            changed_yao=changed.get(
                "yao",
                {},
            ),
        )

    def get_line(
        self,
        result: HexagramResult,
        line: int,
    ) -> dict:
        """
        指定した爻(1〜6)を取得する。
        """

        if line < 1 or line > 6:
            raise ValueError("line は 1〜6 を指定してください。")

        return (
            result.yao
            .get("lines", {})
            .get(str(line), {})
        )

    # ---------------------------------------------------------
    # 変爻取得
    # ---------------------------------------------------------

    def get_changing_lines(
        self,
        result: HexagramResult,
    ) -> list[dict]:
        """
        変爻のみ取得する。
        """

        return [
            self.get_line(result, line)
            for line in result.changing_lines
        ]

    # ---------------------------------------------------------
    # 卦番号から爻取得
    # ---------------------------------------------------------

    def get_line_by_position(
        self,
        hexagram_number: int,
        line: int,
    ) -> dict:
        """
        卦番号と爻番号から取得する。
        """

        if line < 1 or line > 6:
            raise ValueError("line は 1〜6 を指定してください。")

        yao = self.yao.get(
            str(hexagram_number),
            {},
        )

        return (
            yao
            .get("lines", {})
            .get(str(line), {})
        )
    # ---------------------------------------------------------
    # 変卦生成
    # ---------------------------------------------------------

    def get_changed_hexagram(
        self,
        result: HexagramResult,
    ) -> dict:
        """
        本卦から変卦（之卦）を生成する。

        老陰（6）・老陽（9）のみ陰陽を反転する。
        """

        # 陰陽をコピー
        changed_yin_yang = result.yin_yang.copy()

        # 変爻だけ反転
        for line in result.changing_lines:

            index = line - 1

            changed_yin_yang[index] = 1 - changed_yin_yang[index]

        lower_bits = tuple(changed_yin_yang[:3])
        upper_bits = tuple(changed_yin_yang[3:])

        lower_name = self._find_trigram(lower_bits)
        upper_name = self._find_trigram(upper_bits)

        hexagram = self._find_hexagram(
            upper_name,
            lower_name,
        )

        if hexagram is None:
            return {}

        number = hexagram["number"]

        return {

            "number": number,

            "name": hexagram["name"],

            "lower_trigram": lower_name,

            "upper_trigram": upper_name,

            "yin_yang": changed_yin_yang,

            "judgement": self.judgements.get(
                str(number),
                {},
            ),

            "image": self.images.get(
                str(number),
                {},
            ),

            "yao": self.yao.get(
                str(number),
                {},
            ),
        }