# ==========================================================
# Human Readable Verification
# ==========================================================

def print_angle_verification(result):

    print("=" * 70)
    print("LOPAN ANGLE VERIFICATION")
    print("=" * 70)

    print(
        f"入力角度 : {result['input_angle']}°"
    )

    print(
        f"総合状態 : {result['status']}"
    )

    print("-" * 70)

    for layer_id, data in result["layers"].items():

        if data["status"] == "OK":

            record = data["record"]

            print(
                f"Layer {layer_id:02d} : OK"
            )

            print(
                f"  {record}"
            )

        else:

            print(
                f"Layer {layer_id:02d} : "
                f"{data['status']}"
            )

    # ------------------------------------------------------
    # Errors
    # ------------------------------------------------------

    if result["errors"]:

        print()
        print("!!! ERRORS !!!")

        for error in result["errors"]:

            print(
                f"  {error}"
            )

    # ------------------------------------------------------
    # Warnings
    # ------------------------------------------------------

    if result["warnings"]:

        print()
        print("!!! WARNINGS !!!")

        for warning in result["warnings"]:

            print(
                f"  {warning}"
            )

    print("=" * 70)