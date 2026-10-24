# ==========================================================
# Lopan Layer Verification Engine
# Layer 10 ～ Layer 27
# ==========================================================

VERIFICATION_LAYER_START = 10
VERIFICATION_LAYER_END = 27


# ==========================================================
# Angle Normalization
# ==========================================================

def normalize_lopan_angle(angle):
    """
    角度を0°以上360°未満へ正規化する。
    """
    return angle % 360.0


# ==========================================================
# Angle Inclusion
# ==========================================================

def angle_in_range(angle, start, end):
    """
    start → end の角度区間に angle が含まれるか確認する。

    通常区間:
        start < end

    360°を跨ぐ区間:
        start > end

    境界については
        start を含む
        end を原則として次区間へ渡す
    とする。
    """

    angle = normalize_lopan_angle(angle)
    start = normalize_lopan_angle(start)
    end = normalize_lopan_angle(end)

    # 同一角度
    if start == end:
        return True

    # 通常区間
    if start < end:
        return start <= angle < end

    # 360°跨ぎ
    return angle >= start or angle < end


# ==========================================================
# Generic Layer Lookup
# ==========================================================

def find_layer_position(layer_data, angle):
    """
    1つのLayerについて、
    指定された角度に対応するRawデータを探す。
    """

    angle = normalize_lopan_angle(angle)

    for record in layer_data:

        start = record.get("angle_start")
        end = record.get("angle_end")

        if start is None or end is None:
            continue

        if angle_in_range(angle, start, end):
            return record

    return None


# ==========================================================
# Layer 27 Special Lookup
# ==========================================================

def find_layer27_position(angle, raw_layer27):
    """
    Layer 27専用。
    329.5°を起点に1°刻みで検索する。
    """

    angle = normalize_lopan_angle(angle)

    # 329.5°を境にした循環位置
    relative = (angle - 329.5) % 360.0

    index = int(relative // 1.0)

    if index < 0:
        return None

    if index >= len(raw_layer27):
        return None

    return raw_layer27[index]


# ==========================================================
# Layer Registry
# ==========================================================
#
# 各LayerのRawデータをここへ登録する。
#
# ==========================================================

LOPAN_LAYER_REGISTRY = {
    10: "raw_layer10",
    11: "raw_layer11",
    12: "raw_layer12",
    13: "raw_layer13",
    14: "raw_layer14",
    15: "raw_layer15",
    16: "raw_layer16",
    17: "raw_layer17",
    18: "raw_layer18",
    19: "raw_layer19",
    20: "raw_layer20",
    21: "raw_layer21",
    22: "raw_layer22",
    23: "raw_layer23",
    24: "raw_layer24",
    25: "raw_layer25",
    26: "raw_layer26",
    27: "raw_layer27",
}


# ==========================================================
# Verification Result
# ==========================================================

def verify_angle(angle, layer_database):
    """
    指定した1つの角度について
    Layer 10～27を一括照合する。
    """

    angle = normalize_lopan_angle(angle)

    result = {
        "input_angle": angle,
        "layers": {},
        "errors": [],
        "warnings": [],
        "status": "OK",
    }

    # ------------------------------------------------------
    # Layer 10 ～ 27
    # ------------------------------------------------------

    for layer_id in range(
        VERIFICATION_LAYER_START,
        VERIFICATION_LAYER_END + 1,
    ):

        # ----------------------------------------------
        # Layer 27
        # ----------------------------------------------

        if layer_id == 27:

            layer_data = layer_database.get(layer_id)

            if layer_data is None:
                result["layers"][layer_id] = {
                    "status": "NOT_REGISTERED"
                }

                result["warnings"].append(
                    "Layer 27: データ未登録"
                )

                continue

            record = find_layer27_position(
                angle,
                layer_data,
            )

        # ----------------------------------------------
        # Other Layers
        # ----------------------------------------------

        else:

            layer_data = layer_database.get(layer_id)

            if layer_data is None:

                result["layers"][layer_id] = {
                    "status": "NOT_REGISTERED"
                }

                result["warnings"].append(
                    f"Layer {layer_id}: データ未登録"
                )

                continue

            record = find_layer_position(
                layer_data,
                angle,
            )

        # ----------------------------------------------
        # Result
        # ----------------------------------------------

        if record is None:

            result["layers"][layer_id] = {
                "status": "NO_MATCH"
            }

            result["errors"].append(
                f"Layer {layer_id}: "
                f"{angle}° に対応するデータが見つからない"
            )

        else:

            result["layers"][layer_id] = {
                "status": "OK",
                "record": record,
            }

    # ======================================================
    # Overall Status
    # ======================================================

    if result["errors"]:

        result["status"] = "ERROR"

    elif result["warnings"]:

        result["status"] = "WARNING"

    else:

        result["status"] = "OK"

    return result