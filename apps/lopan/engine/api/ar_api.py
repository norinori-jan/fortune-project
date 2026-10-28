"""
Feng Shui AI
Lopan AR Angle Engine API

Purpose
-------
・AR上で現在角度を入力／変更する
・Layer 10〜27を同時に照合する
・角度変更に応じて各Layerの表示内容を更新する
・吉凶を自動判定しない
・意味付けしない
・Raw Databaseを変更しない

Basic Concept
-------------
羅盤は土地・場所などを測定するために使用する。

ARでは、

angle → Layer 10〜27 → 対応データ

という変換だけを担当する。
"""


# ==========================================================
# Configuration
# ==========================================================

AR_ENGINE_VERSION = "AR-AngleEngine-1.0"

ANGLE_MIN = 0.0
ANGLE_MAX = 360.0


# ==========================================================
# Angle Normalization
# ==========================================================

def normalize_angle(angle):
    """
    角度を0°以上360°未満に正規化する。
    """

    angle = float(angle)

    angle = angle % 360.0

    return angle


# ==========================================================
# AR Measurement State
# ==========================================================

class ARMeasurementState:

    def __init__(self, angle=0.0):

        self.angle = normalize_angle(angle)

        self.previous_angle = None

        self.layers = {}

        self.updated = False

    def set_angle(self, angle):

        new_angle = normalize_angle(angle)

        self.previous_angle = self.angle

        self.angle = new_angle

        self.updated = True

    def get_angle(self):

        return self.angle


# ==========================================================
# Layer Lookup
# ==========================================================

def lookup_layers(
    angle,
    database
):
    """
    現在角度における
    Layer 10〜27の対応データを取得する。

    注意：
    各Layerの角度体系は異なるため、
    build_layer_adapter()を使用する。
    """

    angle = normalize_angle(angle)

    results = {}

    for layer_id in range(10, 28):

        adapter = build_layer_adapter(
            layer_id,
            database
        )

        if adapter is None:

            results[layer_id] = {
                "status": "NOT_REGISTERED",
                "matches": []
            }

            continue

        matches = adapter.lookup(
            angle
        )

        results[layer_id] = {

            "status":
                "OK"
                if len(matches) == 1
                else
                "NO_MATCH"
                if len(matches) == 0
                else
                "OVERLAP",

            "matches":
                matches
        }

    return results


# ==========================================================
# AR Angle Update
# ==========================================================

def update_ar_angle(
    state,
    angle,
    database
):
    """
    ARで角度が変化したときに呼び出す。

    例：

    update_ar_angle(
        state,
        72.4,
        database
    )
    """

    state.set_angle(
        angle
    )

    layer_results = lookup_layers(
        state.angle,
        database
    )

    state.layers = layer_results

    return build_ar_response(
        state
    )


# ==========================================================
# AR Response
# ==========================================================

def build_ar_response(
    state
):
    """
    AR UIへ渡すデータ。

    意味付け・吉凶判定はしない。
    """

    return {

        "engine":
            AR_ENGINE_VERSION,

        "measurement": {

            "angle":
                state.angle,

            "previous_angle":
                state.previous_angle
        },

        "layers":
            state.layers,

        "display": {

            "angle_changed":
                state.updated,

            "refresh_required":
                state.updated
        }
    }


# ==========================================================
# Continuous AR Tracking
# ==========================================================

def process_ar_measurement(
    angle,
    database
):
    """
    ARカメラ／センサーから角度が
    連続的に入ってくる場合の簡易入口。

    毎フレーム呼び出してもよい。
    """

    angle = normalize_angle(
        angle
    )

    layers = lookup_layers(
        angle,
        database
    )

    return {

        "angle":
            angle,

        "layers":
            layers
    }


# ==========================================================
# Angle Change Detection
# ==========================================================

def angle_changed(
    previous_angle,
    current_angle,
    threshold=0.05
):
    """
    小さなセンサー揺れを無視するための
    角度変化判定。

    threshold:
    デフォルト 0.05°
    """

    previous_angle = normalize_angle(
        previous_angle
    )

    current_angle = normalize_angle(
        current_angle
    )

    difference = abs(
        current_angle -
        previous_angle
    )

    # 0°/360°境界対応

    difference = min(
        difference,
        360.0 - difference
    )

    return difference >= threshold


# ==========================================================
# AR Measurement Controller
# ==========================================================

class ARAngleController:

    def __init__(
        self,
        database,
        initial_angle=0.0
    ):

        self.database = database

        self.state = ARMeasurementState(
            initial_angle
        )

    def set_angle(
        self,
        angle
    ):

        return update_ar_angle(
            self.state,
            angle,
            self.database
        )

    def get_current(self):

        return {

            "angle":
                self.state.angle,

            "layers":
                self.state.layers
        }


# ==========================================================
# API-style Interface
# ==========================================================

class LopanARAPI:

    def __init__(
        self,
        database
    ):

        self.database = database

        self.controller = ARAngleController(
            database
        )

    # ------------------------------------------------------
    # 現在角度取得
    # ------------------------------------------------------

    def get_angle(self):

        return self.controller.state.angle

    # ------------------------------------------------------
    # 角度設定
    # ------------------------------------------------------

    def set_angle(
        self,
        angle
    ):

        return self.controller.set_angle(
            angle
        )

    # ------------------------------------------------------
    # 全Layer取得
    # ------------------------------------------------------

    def get_layers(self):

        return self.controller.state.layers

    # ------------------------------------------------------
    # 角度＋全Layerを一括取得
    # ------------------------------------------------------

    def measure(
        self,
        angle
    ):

        return self.set_angle(
            angle
        )

    # ------------------------------------------------------
    # 現在状態
    # ------------------------------------------------------

    def state(self):

        return {

            "angle":
                self.controller.state.angle,

            "layers":
                self.controller.state.layers
        }