import os
import sys
from datetime import datetime

current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)

sys.path.append(os.path.join(project_root, "fortune-core"))
sys.path.append(os.path.join(project_root, "fortune-registry"))

from fortune_core.shichu.registry_loader import RegistryLoader
from fortune_core.shichu.engine import Engine
# ------------------------------------------------------------
# 1. モジュール探索パスの設定
# ------------------------------------------------------------
current_dir = os.path.dirname(os.path.abspath(__file__))  # app/
project_root = os.path.dirname(current_dir)               # fortune-project/

# app/
sys.path.append(current_dir)
# fortune-core/
sys.path.append(os.path.join(project_root, "fortune-core"))
# fortune-registry/
sys.path.append(os.path.join(project_root, "fortune-registry"))

# ------------------------------------------------------------
# 2. Engine の読み込み
# ------------------------------------------------------------
try:
    from fortune_core.shichu.engine import Engine
except Exception as e:
    print("❌ Engine の import に失敗しました")
    print("sys.path =", sys.path)
    print(e)
    raise





# ------------------------------------------------------------
# 5. メイン処理
# ------------------------------------------------------------
def main():

    REGISTRY_ROOT = r"C:\Users\norin\fortune-project\fortune-registry"

    

    loader = RegistryLoader(REGISTRY_ROOT)

    engine = Engine(
        registry_loader=loader,
        solar_terms_json_path=SOLAR_TERMS_JSON
    )
    
    test_birth = datetime(1995, 2, 15, 12, 0)
    gender = "男"

    print("--- 鑑定書ロジック実行テスト ---")

    chart = engine.generate(
        birth=test_birth,
        gender=gender
    )

    print(chart)




# ------------------------------------------------------------
# 6. エントリーポイント
# ------------------------------------------------------------
if __name__ == "__main__":
    main()
