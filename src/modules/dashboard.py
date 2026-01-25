import logging
from collections import defaultdict
from datetime import datetime

_LOGGER = logging.getLogger(__name__)


def build_monthly_dashboard(events):
    """
    목적: 이번 달 대시보드 집계를 생성한다.
    Args:
        events (list[dict]): 이벤트 목록
    Returns:
        dict: 집계 결과
    Side Effects:
        없음
    Raises:
        없음
    """
    totals = {"INBOUND": 0, "OUTBOUND": 0, "RETURN": 0}
    now = datetime.now()
    for event in events:
        occurred = _parse_month(event.get("occurred_at"))
        if not occurred or occurred.month != now.month or occurred.year != now.year:
            continue
        event_type = event.get("event_type")
        if event_type in totals:
            totals[event_type] += event.get("quantity") or 0
    return {
        "total_inbound": totals["INBOUND"],
        "total_outbound": totals["OUTBOUND"],
        "total_return": totals["RETURN"],
        "net_change": totals["INBOUND"] - totals["OUTBOUND"] + totals["RETURN"],
    }


def compare_month(events, month_offset=1):
    """
    목적: 전월 대비 증감을 계산한다.
    Args:
        events (list[dict]): 이벤트 목록
        month_offset (int): 비교할 월 오프셋
    Returns:
        dict: 비교 결과
    Side Effects:
        없음
    Raises:
        없음
    """
    current = build_monthly_dashboard(events)
    previous = _build_dashboard_for_offset(events, month_offset)
    return {
        "inbound_diff": current["total_inbound"] - previous["total_inbound"],
        "outbound_diff": current["total_outbound"] - previous["total_outbound"],
        "return_diff": current["total_return"] - previous["total_return"],
        "net_diff": current["net_change"] - previous["net_change"],
    }


def top_turnover_items(events, top_n=10):
    """
    목적: 회전율 상위 품목을 계산한다.
    Args:
        events (list[dict]): 이벤트 목록
        top_n (int): 상위 개수
    Returns:
        list[tuple]: (item_id, score) 목록
    Side Effects:
        없음
    Raises:
        없음
    """
    score = defaultdict(int)
    for event in events:
        item_id = event.get("item_id")
        if not item_id:
            continue
        event_type = event.get("event_type")
        if event_type in {"INBOUND", "OUTBOUND", "RETURN"}:
            score[item_id] += abs(event.get("quantity") or 0)
    return sorted(score.items(), key=lambda item: item[1], reverse=True)[:top_n]


def shortage_items(inventory, items):
    """
    목적: 안전 재고 부족 품목을 계산한다.
    Args:
        inventory (dict): 재고 정보
        items (list[dict]): 품목 마스터
    Returns:
        list[str]: 부족 품목 ID
    Side Effects:
        없음
    Raises:
        없음
    """
    shortages = []
    item_map = {item.get("item_id"): item for item in items}
    for item_id, entry in inventory.items():
        safety = item_map.get(item_id, {}).get("safety_stock", 0)
        if entry.get("total", 0) < safety:
            shortages.append(item_id)
    return shortages


def _build_dashboard_for_offset(events, month_offset):
    """
    목적: 월 오프셋 기준 집계를 생성한다.
    Args:
        events (list[dict]): 이벤트 목록
        month_offset (int): 비교 월 오프셋
    Returns:
        dict: 집계 결과
    Side Effects:
        없음
    Raises:
        없음
    """
    totals = {"INBOUND": 0, "OUTBOUND": 0, "RETURN": 0}
    now = datetime.now()
    target_month = now.month - month_offset
    target_year = now.year
    if target_month <= 0:
        target_month += 12
        target_year -= 1
    for event in events:
        occurred = _parse_month(event.get("occurred_at"))
        if not occurred or occurred.month != target_month or occurred.year != target_year:
            continue
        event_type = event.get("event_type")
        if event_type in totals:
            totals[event_type] += event.get("quantity") or 0
    return {
        "total_inbound": totals["INBOUND"],
        "total_outbound": totals["OUTBOUND"],
        "total_return": totals["RETURN"],
        "net_change": totals["INBOUND"] - totals["OUTBOUND"] + totals["RETURN"],
    }


def _parse_month(value):
    """
    목적: ISO8601 문자열을 datetime으로 변환한다.
    Args:
        value (str): 시간 문자열
    Returns:
        datetime|None: 변환 결과
    Side Effects:
        없음
    Raises:
        없음
    """
    if not value:
        return None
    try:
        return datetime.fromisoformat(value)
    except ValueError:
        _LOGGER.warning("Invalid datetime: %s", value)
        return None
