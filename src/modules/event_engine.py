import logging
from datetime import datetime, timezone
from uuid import uuid4

from config import get_data_dir, get_default_user
from modules import storage

_LOGGER = logging.getLogger(__name__)


def _now_iso():
    """
    목적: 현재 시간을 ISO8601 문자열로 반환한다.
    Args:
        없음
    Returns:
        str: ISO8601 시간 문자열
    Side Effects:
        없음
    Raises:
        없음
    """
    return datetime.now(timezone.utc).isoformat()


def record_event(event):
    """
    목적: 이벤트를 기록하고 영구 저장한다.
    Args:
        event (dict): 이벤트 데이터
    Returns:
        dict|None: 기록된 이벤트
    Side Effects:
        events.json 쓰기
    Raises:
        없음
    """
    if not event:
        return None
    event_id = event.get("event_id") or str(uuid4())
    payload = {
        "event_id": event_id,
        "event_type": event.get("event_type"),
        "occurred_at": event.get("occurred_at") or _now_iso(),
        "item_id": event.get("item_id"),
        "quantity": event.get("quantity"),
        "unit": event.get("unit"),
        "location_id": event.get("location_id"),
        "reference_type": event.get("reference_type") or "NONE",
        "reference_id": event.get("reference_id"),
        "created_by": event.get("created_by") or get_default_user(),
        "reason": event.get("reason") or "",
        "reverses_event_id": event.get("reverses_event_id"),
    }
    data_dir = get_data_dir()
    events_path = data_dir / "events.json"
    if not storage.append_json_list(events_path, payload):
        _LOGGER.error("Failed to append event")
        return None
    for line in event.get("lines", []):
        line_payload = {"event_id": event_id, **line}
        storage.append_json_list(data_dir / "event_lines.json", line_payload)
    return payload


def replay_inventory(events):
    """
    목적: 이벤트를 재생하여 현재 재고를 계산한다.
    Args:
        events (list[dict]): 이벤트 목록
    Returns:
        dict: item_id 기반 재고 정보
    Side Effects:
        없음
    Raises:
        없음
    """
    inventory = {}
    events_by_id = {event.get("event_id"): event for event in events if event.get("event_id")}
    for event in events:
        event_type = event.get("event_type")
        if event_type == "ORDER":
            continue
        if event_type == "REVERSAL":
            original = events_by_id.get(event.get("reverses_event_id"))
            if original:
                _apply_event(inventory, original, reverse=True)
            else:
                _LOGGER.warning("Reversal missing original: %s", event.get("reverses_event_id"))
            continue
        _apply_event(inventory, event)
    return inventory


def reverse_event(event_id):
    """
    목적: 특정 이벤트의 되돌림 이벤트를 기록한다.
    Args:
        event_id (str): 되돌릴 이벤트 ID
    Returns:
        dict|None: 되돌림 이벤트
    Side Effects:
        events.json 쓰기
    Raises:
        없음
    """
    data = storage.load_all_data()
    events = data.get("events", [])
    if not events:
        return None
    target = next((event for event in events if event.get("event_id") == event_id), None)
    if not target:
        return None
    for event in events:
        if event.get("event_type") == "REVERSAL" and event.get("reverses_event_id") == event_id:
            return None
    reversal = {
        "event_type": "REVERSAL",
        "item_id": target.get("item_id"),
        "quantity": target.get("quantity"),
        "unit": target.get("unit"),
        "location_id": target.get("location_id"),
        "reference_type": target.get("reference_type"),
        "reference_id": target.get("reference_id"),
        "reason": f"Reverse {event_id}",
        "reverses_event_id": event_id,
    }
    return record_event(reversal)


def _apply_event(inventory, event, reverse=False):
    """
    목적: 이벤트를 재고에 적용한다.
    Args:
        inventory (dict): 재고 상태
        event (dict): 이벤트 데이터
        reverse (bool): 역적용 여부
    Returns:
        None
    Side Effects:
        inventory 수정
    Raises:
        없음
    """
    item_id = event.get("item_id")
    if not item_id:
        return
    quantity = event.get("quantity") or 0
    if reverse:
        quantity = -quantity
    if item_id not in inventory:
        inventory[item_id] = {"total": 0, "locations": {}, "unit": event.get("unit")}
    entry = inventory[item_id]
    event_type = event.get("event_type")
    location_id = event.get("location_id") or "UNSPECIFIED"
    if event_type == "INBOUND":
        entry["total"] += quantity
        entry["locations"][location_id] = entry["locations"].get(location_id, 0) + quantity
    elif event_type == "OUTBOUND":
        entry["total"] -= quantity
        entry["locations"][location_id] = entry["locations"].get(location_id, 0) - quantity
    elif event_type == "RETURN":
        return_type = event.get("reference_type") or "RETURN_CUSTOMER"
        direction = 1 if return_type == "RETURN_CUSTOMER" else -1
        entry["total"] += quantity * direction
        entry["locations"][location_id] = entry["locations"].get(location_id, 0) + quantity * direction
    elif event_type == "MOVE":
        from_location = event.get("reference_id") or "UNSPECIFIED"
        entry["locations"][from_location] = entry["locations"].get(from_location, 0) - quantity
        entry["locations"][location_id] = entry["locations"].get(location_id, 0) + quantity
