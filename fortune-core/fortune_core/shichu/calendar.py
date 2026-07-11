from datetime import timedelta

LONGITUDE = {

    "tokyo": 18,

    "osaka": 2,

    "nagoya": 8,

    "sendai": 20,

    "sapporo": 25,

    "hiroshima": -6,

    "fukuoka": -18,

    "naha": -29

}


def adjust_longitude(
    birth,
    city=None
):

    if city is None:
        return birth

    minute = LONGITUDE.get(
        city.lower(),
        0
    )

    return birth + timedelta(
        minutes=minute
    )