from dataclasses import dataclass

from fortune_core.shichu.dataclasses import Chart, ElementStrength


class ElementStrengthAnalyzer:
    """
    五行量解析

    ・天干 1.0
    ・地支 1.0
    ・蔵干 0.5

    将来的に
    ・月令補正
    ・旺相休囚死
    ・通根
    ・透干
    ・会局
    ・方合
    を追加する。
    """

    def __init__(self, registry_loader):
        self.registry_loader = registry_loader

    # ------------------------------------------------------------
    # 五行量
    # ------------------------------------------------------------
    def analyze(self, chart: Chart) -> ElementStrength:

        values = {
            "木": 0.0,
            "火": 0.0,
            "土": 0.0,
            "金": 0.0,
            "水": 0.0,
        }

        pillars = [
            chart.year,
            chart.month,
            chart.day,
            chart.hour,
        ]

        stems = self.registry_loader.get_stems()

        for pillar in pillars:

            # -------------------------
            # 天干
            # -------------------------
            values[pillar.stem.element] += 1.0

            # -------------------------
            # 地支
            # -------------------------
            values[pillar.branch.element] += 1.0

            # -------------------------
            # 蔵干
            # -------------------------
            zang = getattr(pillar, "zangkan", None)

            if zang:

                if isinstance(zang, str):

                    stem = stems.get(zang)

                    if stem:
                        values[stem.element] += 0.5

                else:

                    for s in (
                        getattr(zang, "main", None),
                        getattr(zang, "middle", None),
                        getattr(zang, "extra", None),
                    ):

                        if s is not None:
                            values[s.element] += 0.5

        return ElementStrength(values=values)