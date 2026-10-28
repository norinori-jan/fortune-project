# ==========================================================
# Feng Shui AI
# Lopan Angle Integrity Scanner
#
# Layer 10 ～ Layer 27
#
# IMPORTANT
# ----------
# 各Layerは同じ角度構造ではない。
# Layer固有の定義を使用して検査する。
#
# Raw Dataは変更しない。
# 本モジュールは検査専用。
# ==========================================================

import math

LAYER_START = 10
LAYER_END = 27

SCAN_START = 0.0
SCAN_END = 360.0
SCAN_STEP = 0.1

EPSILON = 1e-7

# ==========================================================
# Angle Utility
# ==========================================================

def normalize_angle(angle):
    return angle % 360.0


def angle_equal(a, b):
    return abs(normalize_angle(a) - normalize_angle(b)) <= EPSILON


def circular_distance(a, b):
    """
    2つの角度の最短距離。
    """
    a = normalize_angle(a)
    b = normalize_angle(b)

    d = abs(a - b)
    return min(d, 360.0 - d)


# ==========================================================
# Generic Circular Range
# ==========================================================

def angle_in_range(angle, start, end):
    angle = normalize_angle(angle)
    start = normalize_angle(start)
    end = normalize_angle(end)

    if start < end:
        return start <= angle < end

    if start > end:
        return angle >= start or angle < end

    return True


# ==========================================================
# Layer Adapter Base
# ==========================================================

class LayerAdapter:
    layer_id = None

    def lookup(self, angle):
        raise NotImplementedError

    def validate(self):
        raise NotImplementedError


# ==========================================================
# 1. Standard Angle Layer
# ==========================================================

class StandardAngleLayerAdapter(LayerAdapter):

    def __init__(self, layer_id, records):
        self.layer_id = layer_id
        self.records = records

    def lookup(self, angle):
        matches = []

        for index, record in enumerate(self.records):
            start = record.get("angle_start")
            end = record.get("angle_end")

            if start is None or end is None:
                continue

            if angle_in_range(angle, start, end):
                matches.append({"index": index, "record": record})

        return matches

    def validate(self):
        return validate_standard_records(self.records)


# ==========================================================
# 2. Equal Division Layer
# ==========================================================

class EqualDivisionLayerAdapter(LayerAdapter):

    def __init__(self, layer_id, start_angle, width, count, records=None):
        self.layer_id = layer_id
        self.start_angle = start_angle
        self.width = width
        self.count = count
        self.records = records or []

    def lookup(self, angle):
        relative = (normalize_angle(angle) - normalize_angle(self.start_angle)) % 360.0
        index = int(relative / self.width)

        if index >= self.count:
            return []

        if self.records:
            if index >= len(self.records):
                return []
            return [{"index": index, "record": self.records[index]}]

        return [{
            "index": index,
            "record": {
                "segment": index + 1,
                "angle_start": normalize_angle(self.start_angle + index * self.width),
                "angle_end": normalize_angle(self.start_angle + (index + 1) * self.width)
            }
        }]

    def validate(self):
        errors = []
        warnings = []

        expected = self.count
        actual = len(self.records)

        if self.records and actual != expected:
            errors.append({
                "type": "RECORD_COUNT",
                "expected": expected,
                "actual": actual
            })

        return {
            "status": "ERROR" if errors else "WARNING" if warnings else "OK",
            "errors": errors,
            "warnings": warnings
        }


# ==========================================================
# 3. Layer 14
# ==========================================================

class Layer14Adapter(StandardAngleLayerAdapter):

    def __init__(self, records):
        super().__init__(layer_id=14, records=records)


# ==========================================================
# 4. Layer 24
# ==========================================================

class Layer24Adapter(EqualDivisionLayerAdapter):

    def __init__(self, records):
        super().__init__(
            layer_id=24,
            start_angle=330.0,
            width=15.0,
            count=24,
            records=records
        )


# ==========================================================
# 5. Layer 25
# ==========================================================

class Layer25Adapter(StandardAngleLayerAdapter):

    def __init__(self, records):
        super().__init__(layer_id=25, records=records)


# ==========================================================
# 6. Layer 26
# ==========================================================

class Layer26Adapter(LayerAdapter):

    def __init__(self, records, start_angle=329.5):
        self.layer_id = 26
        self.records = records
        self.start_angle = start_angle

    def lookup(self, angle):
        relative = (normalize_angle(angle) - normalize_angle(self.start_angle)) % 360.0
        index = int(relative // 1.0)

        if index >= len(self.records):
            return []

        return [{"index": index, "record": self.records[index]}]

    def validate(self):
        errors = []

        if len(self.records) > 360:
            errors.append({"type": "TOO_MANY_RECORDS", "count": len(self.records)})

        return {
            "status": "ERROR" if errors else "OK",
            "errors": errors,
            "warnings": []
        }


# ==========================================================
# 7. Layer 27
# ==========================================================

class Layer27Adapter(Layer26Adapter):

    def __init__(self, records, start_angle=329.5):
        super().__init__(records=records, start_angle=start_angle)
        self.layer_id = 27


# ==========================================================
# Standard Record Validation
# ==========================================================

def validate_standard_records(records):
    errors = []
    warnings = []
    valid = []

    for index, record in enumerate(records):
        start = record.get("angle_start")
        end = record.get("angle_end")

        if start is None or end is None:
            warnings.append({"type": "MISSING_ANGLE", "index": index})
            continue

        valid.append((index, normalize_angle(start), normalize_angle(end)))

    # Overlap detection
    for i in range(len(valid)):
        index_a, start_a, end_a = valid[i]

        for j in range(i + 1, len(valid)):
            index_b, start_b, end_b = valid[j]

            overlap_found = False

            for test_angle in (start_a, end_a, start_b, end_b):
                test_angle = normalize_angle(test_angle + EPSILON)

                if angle_in_range(test_angle, start_a, end_a) and angle_in_range(test_angle, start_b, end_b):
                    overlap_found = True
                    break

            if overlap_found:
                errors.append({
                    "type": "OVERLAP",
                    "record_a": index_a,
                    "record_b": index_b
                })

    return {
        "status": "ERROR" if errors else "WARNING" if warnings else "OK",
        "errors": errors,
        "warnings": warnings
    }


# ==========================================================
# Layer Adapter Factory
# ==========================================================

def build_layer_adapter(layer_id, database):
    records = database.get(layer_id)

    if records is None:
        return None

    if layer_id == 14:
        return Layer14Adapter(records)

    if layer_id == 24:
        return Layer24Adapter(records)

    if layer_id == 26:
        return Layer26Adapter(records)

    if layer_id == 27:
        return Layer27Adapter(records)

    if layer_id == 25:
        return Layer25Adapter(records)

    return StandardAngleLayerAdapter(layer_id, records)


# ==========================================================
# Single Angle Verification
# ==========================================================

def verify_all_layers(angle, database):
    angle = normalize_angle(angle)

    result = {
        "input_angle": angle,
        "layers": {},
        "errors": [],
        "warnings": [],
        "status": "OK"
    }

    for layer_id in range(LAYER_START, LAYER_END + 1):
        adapter = build_layer_adapter(layer_id, database)

        if adapter is None:
            result["layers"][layer_id] = {"status": "NOT_REGISTERED"}
            result["warnings"].append(f"Layer {layer_id}: 未登録")
            continue

        matches = adapter.lookup(angle)

        result["layers"][layer_id] = {
            "status": "OK" if len(matches) == 1 else "NO_MATCH" if len(matches) == 0 else "OVERLAP",
            "matches": matches
        }

        if len(matches) == 0:
            result["errors"].append(f"Layer {layer_id}: NO_MATCH")
        elif len(matches) > 1:
            result["errors"].append(f"Layer {layer_id}: OVERLAP")

    if result["errors"]:
        result["status"] = "ERROR"
    elif result["warnings"]:
        result["status"] = "WARNING"

    return result


# ==========================================================
# Full 360° Integrity Scan
# ==========================================================

def scan_full_circle(database, step=0.1):
    result = {
        "step": step,
        "layers": {},
        "global_status": "OK"
    }

    # Structure validation
    for layer_id in range(LAYER_START, LAYER_END + 1):
        adapter = build_layer_adapter(layer_id, database)

        if adapter is None:
            result["layers"][layer_id] = {
                "status": "NOT_REGISTERED",
                "structure": None,
                "holes": [],
                "overlaps": []
            }
            result["global_status"] = "ERROR"
            continue

        structure = adapter.validate()

        result["layers"][layer_id] = {
            "status": structure["status"],
            "structure": structure,
            "holes": [],
            "overlaps": []
        }

    # 0°〜360° scan
    steps = int(math.ceil(360.0 / step))

    for n in range(steps):
        angle = n * step
        if angle >= 360.0:
            break

        for layer_id in range(LAYER_START, LAYER_END + 1):
            adapter = build_layer_adapter(layer_id, database)
            if adapter is None:
                continue

            matches = adapter.lookup(angle)

            if len(matches) == 0:
                result["layers"][layer_id]["holes"].append(angle)
            elif len(matches) > 1:
                result["layers"][layer_id]["overlaps"].append({
                    "angle": angle,
                    "matches": matches
                })

    # Final status
    for layer_id, data in result["layers"].items():
        if data["holes"] or data["overlaps"]:
            data["status"] = "ERROR"
            result["global_status"] = "ERROR"

    return result


# ==========================================================
# Report
# ==========================================================

def print_integrity_report(result):
    print()
    print("=" * 78)
    print("LOPAN ANGLE INTEGRITY SCAN")
    print("=" * 78)

    print(f"Scan step : {result['step']}°")
    print(f"Global : {result['global_status']}")
    print("-" * 78)

    for layer_id in sorted(result["layers"]):
        data = result["layers"][layer_id]

        print(f"Layer {layer_id:02d} : {data['status']}")

        if data["holes"]:
            print(f" holes = {len(data['holes'])}")
            print(f" sample = {data['holes'][:15]}")

        if data["overlaps"]:
            print(f" overlaps = {len(data['overlaps'])}")
            print(f" sample = {data['overlaps'][:5]}")

        print("=" * 78)
