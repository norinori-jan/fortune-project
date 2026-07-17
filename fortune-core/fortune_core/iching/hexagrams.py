# fortune_core/iching/hexagrams.py

from dataclasses import dataclass

from .registry_loader import RegistryLoader


@dataclass(frozen=True)
class HexagramResult:

    numbers: list[int]

    upper_trigram: str

    lower_trigram: str

    hexagram_number: int

    hexagram_name: str

    judgement: str

    image: str

    changing_lines: list[int]


class HexagramEngine:
    """
    易経エンジン
    """

    def __init__(self):

        self.registry = RegistryLoader()

        self.trigrams = self.registry.get_trigrams()

    # ---------------------------------------------------------
    # 陰陽配列から八卦を取得
    # ---------------------------------------------------------

    def _find_trigram(self, bits):

        for name, data in self.trigrams.items():

            if tuple(data["binary"]) == bits:

                return name

        return "不明"

    # ---------------------------------------------------------
    # 六爻→卦
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

        lower = tuple(
            yin_yang[:3]
        )

        upper = tuple(
            yin_yang[3:]
        )

        lower_name = self._find_trigram(lower)

        upper_name = self._find_trigram(upper)

        changing = [

            i + 1

            for i, value in enumerate(numbers)

            if value in (6, 9)

        ]

        return HexagramResult(

            numbers=numbers,

            upper_trigram=upper_name,

            lower_trigram=lower_name,

            hexagram_number=0,

            hexagram_name="未判定",

            judgement="64卦実装後に表示",

            image="",

            changing_lines=changing,
        )