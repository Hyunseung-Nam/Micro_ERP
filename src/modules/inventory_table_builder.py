"""
재고 테이블용 행 데이터 생성.
UI와 무관한 순수 로직으로, 테스트 및 재사용이 용이하다.
"""

INVENTORY_TABLE_HEADERS = [
    "품목 ID",
    "품목명",
    "카테고리",
    "현재고",
    "단위",
    "안전재고",
    "권장발주",
    "위치별 재고",
]


def build_inventory_rows(inventory, items, search_text, shortage_ids):
    """
    재고/품목 마스터와 검색어·안전재고 부족 집합으로 테이블 행 목록을 만든다.

    Args:
        inventory: item_id -> { total, locations, unit }
        items: 품목 마스터 리스트
        search_text: 검색어 (소문자, 공백 제거)
        shortage_ids: 안전재고 부족 품목 ID 집합

    Returns:
        list[dict]: 각 행은 item_id, item_name, category, total, unit,
                    safety, recommended, locations, is_low 키를 가진다.
    """
    item_map = {item.get("item_id"): item for item in items if item.get("item_id")}
    search_lower = (search_text or "").strip().lower()
    merged_ids = sorted(set(item_map.keys()) | set(inventory.keys()))
    rows = []

    for item_id in merged_ids:
        entry = inventory.get(item_id, {"total": 0, "locations": {}, "unit": ""})
        meta = item_map.get(item_id, {})
        item_name = meta.get("item_name", "")
        category = meta.get("category", "")
        locations = ", ".join(
            f"{loc}:{qty}" for loc, qty in sorted(entry.get("locations", {}).items()) if qty != 0
        ) or "-"
        safety = int(meta.get("safety_stock", 0) or 0)
        total = int(entry.get("total", 0) or 0)
        reorder_qty = int(meta.get("reorder_qty", 0) or 0)
        recommended = max(safety - total, 0)
        if recommended == 0 and total < safety and reorder_qty > 0:
            recommended = reorder_qty

        searchable = " ".join([item_id, item_name, category, locations]).lower()
        if search_lower and search_lower not in searchable:
            continue

        rows.append({
            "item_id": item_id,
            "item_name": item_name or "-",
            "category": category or "-",
            "total": total,
            "unit": entry.get("unit") or meta.get("unit") or "-",
            "safety": safety,
            "recommended": recommended,
            "locations": locations,
            "is_low": item_id in shortage_ids,
        })

    return rows
