# ==========================================================
# Integrity Report
# ==========================================================

def print_integrity_report(result):

    print()
    print("=" * 72)
    print("LOPAN ANGLE INTEGRITY SCAN")
    print("=" * 72)

    print(
        f"Scan : "
        f"{result['scan']['start']}°"
        f" ～ "
        f"{result['scan']['end']}°"
    )

    print(
        f"Step : "
        f"{result['scan']['step']}°"
    )

    print(
        f"GLOBAL STATUS : "
        f"{result['global_status']}"
    )

    print("-" * 72)

    for layer_id, data in result["layers"].items():

        print(
            f"Layer {layer_id:02d} : "
            f"{data['status']}"
        )

        if data["status"] == "NOT_REGISTERED":
            continue

        scan = data["scan"]

        # ----------------------------------------------
        # Holes
        # ----------------------------------------------

        if scan["holes"]:

            print(
                f"  HOLES : "
                f"{len(scan['holes'])}"
            )

            print(
                f"  sample : "
                f"{scan['holes'][:20]}"
            )

        # ----------------------------------------------
        # Overlaps
        # ----------------------------------------------

        if scan["overlaps"]:

            print(
                f"  OVERLAPS : "
                f"{len(scan['overlaps'])}"
            )

            for item in scan["overlaps"][:10]:

                print(
                    f"    {item['angle']}°"
                )

        # ----------------------------------------------
        # Invalid records
        # ----------------------------------------------

        if scan["invalid_records"]:

            print(
                f"  INVALID RECORDS : "
                f"{len(scan['invalid_records'])}"
            )

        # ----------------------------------------------
        # Boundaries
        # ----------------------------------------------

        boundary = data["boundaries"]

        if boundary["duplicate_boundaries"]:

            print(
                f"  DUPLICATE BOUNDARIES : "
                f"{len(boundary['duplicate_boundaries'])}"
            )

    print("=" * 72)