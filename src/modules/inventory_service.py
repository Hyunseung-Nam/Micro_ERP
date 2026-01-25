import logging

from modules import event_engine, storage, validator

_LOGGER = logging.getLogger(__name__)


def apply_inbound(payload):
    """
    목적: 입고 이벤트를 생성하고 기록한다.
    Args:
        payload (dict): 입고 데이터
    Returns:
        dict|None: 기록된 이벤트
    Side Effects:
        events.json 쓰기
    Raises:
        없음
    """
    error = validator.validate_inbound(payload)
    if error:
        _LOGGER.warning("Inbound validation failed: %s", error)
        return None
    event = {
        "event_type": "INBOUND",
        "item_id": payload["item_id"],
        "quantity": payload["quantity"],
        "unit": payload["unit"],
        "location_id": payload["location_id"],
        "reference_type": "ORDER" if payload.get("order_id") else "NONE",
        "reference_id": payload.get("order_id"),
        "reason": payload.get("reason", ""),
    }
    return event_engine.record_event(event)


def apply_outbound(payload):
    """
    목적: 출고 이벤트를 생성하고 기록한다.
    Args:
        payload (dict): 출고 데이터
    Returns:
        dict|None: 기록된 이벤트
    Side Effects:
        events.json 쓰기
    Raises:
        없음
    """
    error = validator.validate_outbound(payload)
    if error:
        _LOGGER.warning("Outbound validation failed: %s", error)
        return None
    if not _has_sufficient_stock(payload):
        _LOGGER.warning("Insufficient stock for outbound")
        return None
    event = {
        "event_type": "OUTBOUND",
        "item_id": payload["item_id"],
        "quantity": payload["quantity"],
        "unit": payload["unit"],
        "location_id": payload["location_id"],
        "reference_type": "NONE",
        "reference_id": None,
        "reason": payload.get("reason", ""),
    }
    return event_engine.record_event(event)


def apply_move(payload):
    """
    목적: 이동 이벤트를 생성하고 기록한다.
    Args:
        payload (dict): 이동 데이터
    Returns:
        dict|None: 기록된 이벤트
    Side Effects:
        events.json 쓰기
    Raises:
        없음
    """
    error = validator.validate_move(payload)
    if error:
        _LOGGER.warning("Move validation failed: %s", error)
        return None
    if not _has_sufficient_stock(payload, location_key="from_location"):
        _LOGGER.warning("Insufficient stock for move")
        return None
    event = {
        "event_type": "MOVE",
        "item_id": payload["item_id"],
        "quantity": payload["quantity"],
        "unit": payload["unit"],
        "location_id": payload["to_location"],
        "reference_type": "MOVE",
        "reference_id": payload["from_location"],
        "reason": payload.get("reason", ""),
    }
    return event_engine.record_event(event)


def apply_return(payload):
    """
    목적: 반품 이벤트를 생성하고 기록한다.
    Args:
        payload (dict): 반품 데이터
    Returns:
        dict|None: 기록된 이벤트
    Side Effects:
        events.json 쓰기
    Raises:
        없음
    """
    error = validator.validate_return(payload)
    if error:
        _LOGGER.warning("Return validation failed: %s", error)
        return None
    return_type = payload.get("return_type", "CUSTOMER")
    reference_type = "RETURN_CUSTOMER" if return_type == "CUSTOMER" else "RETURN_SUPPLIER"
    if reference_type == "RETURN_SUPPLIER" and not _has_sufficient_stock(payload):
        _LOGGER.warning("Insufficient stock for supplier return")
        return None
    event = {
        "event_type": "RETURN",
        "item_id": payload["item_id"],
        "quantity": payload["quantity"],
        "unit": payload["unit"],
        "location_id": payload["location_id"],
        "reference_type": reference_type,
        "reference_id": payload.get("partner_id"),
        "reason": payload.get("reason", ""),
    }
    return event_engine.record_event(event)


def check_safety_stock(inventory, items):
    """
    목적: 안전 재고 부족 품목을 반환한다.
    Args:
        inventory (dict): 재고 정보
        items (list): 품목 마스터 목록
    Returns:
        list[str]: 부족 품목 ID 리스트
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


def rebuild_inventory(events):
    """
    목적: 이벤트를 재생성하여 재고를 재구축한다.
    Args:
        events (list[dict]): 이벤트 목록
    Returns:
        dict: 재고 정보
    Side Effects:
        없음
    Raises:
        없음
    """
    return event_engine.replay_inventory(events)


def _has_sufficient_stock(payload, location_key="location_id"):
    """
    목적: 재고가 충분한지 확인한다.
    Args:
        payload (dict): 입력 데이터
        location_key (str): 위치 키
    Returns:
        bool: 충분 여부
    Side Effects:
        없음
    Raises:
        없음
    """
    data = storage.load_all_data()
    inventory = event_engine.replay_inventory(data.get("events", []))
    item_id = payload.get("item_id")
    location = payload.get(location_key)
    if not item_id:
        return False
    entry = inventory.get(item_id, {})
    if location:
        return entry.get("locations", {}).get(location, 0) >= payload.get("quantity", 0)
    return entry.get("total", 0) >= payload.get("quantity", 0)
