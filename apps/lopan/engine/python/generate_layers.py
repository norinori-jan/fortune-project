import json
import os

MASTER_FILE = "../data/master/lopan_master.json"
OUTPUT_DIR = "../data/layers"

def load_master():

    with open(
        MASTER_FILE,
        "r",
        encoding="utf-8"
    ) as f:

        return json.load(f)

def save_layer(number,data):

    filename = os.path.join(
        OUTPUT_DIR,
        f"layer{number:02d}.json"
    )

    with open(
        filename,
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            data,
            f,
            ensure_ascii=False,
            indent=2
        )

def make_layer01(master):

    return [

        {

            "id":r["id"],

            "start":r["start_angle"],
            "end":r["end_angle"],

            "text":r["ganchu"]

        }

        for r in master
    ]

def make_layer02(master):

    return [

        {

            "id":r["id"],

            "start":r["start_angle"],
            "end":r["end_angle"],

            "text":r["kyusei"]

        }

        for r in master
    ]

def make_layer03(master):

    return [

        {

            "id":r["id"],

            "start":r["start_angle"],
            "end":r["end_angle"],

            "text":r["unsu"]

        }

        for r in master
    ]

def make_layer04(master):

    return [

        {

            "id":r["id"],

            "start":r["start_angle"],
            "end":r["end_angle"],

            "text":r["kokei"]

        }

        for r in master
    ]

def make_layer23(master):

    return [

        {

            "id":r["id"],

            "start":r["start_angle"],
            "end":r["end_angle"],

            "text":r["host"]

        }

        for r in master
    ]

def make_layer24(master):

    return [

        {

            "id":r["id"],

            "start":r["start_angle"],
            "end":r["end_angle"],

            "text":r["solar_term"]

        }

        for r in master
    ]

def main():

    os.makedirs(
        OUTPUT_DIR,
        exist_ok=True
    )

    master = load_master()

    save_layer(1,make_layer01(master))
    save_layer(2,make_layer02(master))
    save_layer(3,make_layer03(master))
    save_layer(4,make_layer04(master))
    save_layer(23,make_layer23(master))
    save_layer(24,make_layer24(master))

    print("Layers Generated")

