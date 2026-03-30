"""
리팩터링 검증: 새 모듈 로딩 및 재고 행 빌더 동작이 기존과 동일한지 확인한다.
실행: cd Micro_ERP && python3 tests/verify_refactor.py
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

def main():
    from modules.inventory_table_builder import build_inventory_rows, INVENTORY_TABLE_HEADERS
    from modules import inventory_service

    inventory = {"ITEM-A": {"total": 10, "locations": {"WH1": 10}, "unit": "EA"}}
    items = [
        {"item_id": "ITEM-A", "item_name": "품목A", "category": "일반", "safety_stock": 5, "reorder_qty": 10, "unit": "EA"},
    ]
    shortages = set(inventory_service.check_safety_stock(inventory, items))
    rows = build_inventory_rows(inventory, items, "", shortages)

    assert len(rows) == 1, "행 1개"
    assert rows[0]["item_id"] == "ITEM-A" and rows[0]["total"] == 10, "행 내용"
    assert rows[0]["is_low"] is False, "안전재고 충족 시 is_low False"
    assert len(INVENTORY_TABLE_HEADERS) == 8, "헤더 8개"

    # 검색 필터
    rows_filtered = build_inventory_rows(inventory, items, "품목A", shortages)
    assert len(rows_filtered) == 1
    rows_nomatch = build_inventory_rows(inventory, items, "없는단어", shortages)
    assert len(rows_nomatch) == 0

    # DialogHelper 존재 (PySide6 있을 때만 import)
    try:
        from ui.dialog_helpers import DialogHelper
        assert callable(DialogHelper) and DialogHelper.__init__
    except ImportError:
        pass  # PySide6 미설치 환경에서는 스킵

    # Controller가 새 모듈 사용
    controller_path = Path(__file__).resolve().parents[1] / "src" / "modules" / "controller.py"
    controller_src = controller_path.read_text(encoding="utf-8")
    assert "build_inventory_rows" in controller_src and "DialogHelper" in controller_src

    print("verify_refactor: OK")

if __name__ == "__main__":
    main()
