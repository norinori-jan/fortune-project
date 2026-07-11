from datetime import datetime

from ..chart import Chart

from .calendar import adjust_longitude

from .tenkan import (

    get_year_stem_branch,

    get_month_stem_branch,

    get_day_stem_branch,

    get_hour_stem_branch

)


class Engine:
    """
    四柱命式生成エンジン

    Responsibility
    --------------

    ・経度補正

    ・年柱生成

    ・月柱生成

    ・日柱生成

    ・時柱生成

    ・Chart生成
    """

    @staticmethod
    def generate(

        birth: datetime,

        gender: str,

        longitude=None

    ) -> Chart:

        birth = adjust_longitude(

            birth,

            longitude

        )

        year = get_year_stem_branch(

            birth

        )

        month = get_month_stem_branch(

            birth,

            year.stem

        )

        day = get_day_stem_branch(

            birth

        )

        hour = get_hour_stem_branch(

            birth,

            day.stem

        )

        return Chart(

            birth=birth,

            gender=gender,

            year=year,

            month=month,

            day=day,

            hour=hour

        )