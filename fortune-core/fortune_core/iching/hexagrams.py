# fortune_core/iching/hexagrams.py

from __future__ import annotations

from dataclasses import dataclass

from .registry_loader import RegistryLoader


@dataclass(frozen=True)
class HexagramResult:
    """
    易経鑑定結果
    """

    numbers: list[int]

    yin_yang: list[int]

    lower_trigram: str
    upper_trigram: str

    hexagram_number: int
    hexagram_name: str

    judgement: str
    image: str

    changing_lines: list[int]


class HexagramEngine:
    """
    易経エンジン

    RegistryLoader から
        ・八卦
        ・六十四卦
        ・卦辞
        ・象伝
        ・爻辞
    を読み込む。
    """

    def __init__(self):

        registry = RegistryLoader()

        self.trigrams = registry.load_trigrams()

        self.hexagrams = registry.load_hexagrams()

        self.judgements = registry.load_judgements()

        self.images = registry.load_images()

        self.yao = registry.load_yao()

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

        raise ValueError(
            f"Unknown trigram: {bits}"
        )

    # ---------------------------------------------------------
    # 六十四卦検索
    # ---------------------------------------------------------

    def _find_hexagram(
        self,
        upper: str,
        lower: str,
    ):

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

            raise ValueError(
                "6本の爻が必要です。"
            )

        yin_yang = [

            1 if n % 2 else 0

            for n in numbers

        ]

        lower_bits = tuple(
            yin_yang[:3]
        )

        upper_bits = tuple(
            yin_yang[3:]
        )

        lower_name = self._find_trigram(
            lower_bits
        )

        upper_name = self._find_trigram(
            upper_bits
        )

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

                judgement="",

                image="",

                changing_lines=changing_lines,
            )

        number = hexagram["number"]

        name = hexagram["name"]

        judgement = self.judgements.get(
            str(number),
            "",
        )

        image = self.images.get(
            str(number),
            "",
        )

        return HexagramResult(

            numbers=numbers,

            yin_yang=yin_yang,

            lower_trigram=lower_name,

            upper_trigram=upper_name,

            hexagram_number=number,

            hexagram_name=name,

            judgement=judgement,

            image=image,

            changing_lines=changing_lines,
        )