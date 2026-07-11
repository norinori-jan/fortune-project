"""
四柱生成

Step3ではインターフェースのみ実装。

Step4でHTML版JavaScriptをPythonへ移植する。
"""

from ..pillar import Pillar


def get_year_stem_branch(birth):

    raise NotImplementedError


def get_month_stem_branch(
    birth,
    year_stem
):

    raise NotImplementedError


def get_day_stem_branch(
    birth
):

    raise NotImplementedError


def get_hour_stem_branch(
    birth,
    day_stem
):

    raise NotImplementedError