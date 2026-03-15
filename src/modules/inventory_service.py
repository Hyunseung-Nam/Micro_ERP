import logging

from modules import event_engine, storage, validator
from modules.service_result import ServiceResult

_LOGGER = logging.getLogger(__name__)


def apply_inbound(payload):
    """입고 이벤트를 생성하고 기록한다."""
    error = validator.validate_inbound(payload)
    if error:
        _LOGGER.warning("Inbound validation failed: %s", error)
        return ServiceResult(ok=False, message=error)

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
    saved = event_engine.record_event(event)
    if not saved:
        return ServiceResult(ok=False, message="입고를 저장하지 못했습니다. 로그를 확인해 주세요.")
    return ServiceResult(ok=True, message="입고가 등록되었습니다.", payload=saved)


def apply_outbound(payload):
    """출고 이벤트를 생성하고 기록한다."""
    error = validator.validate_outbound(payload)
    if error:
        _LOGGER.warning("Outbound validation failed: %s", error)
        return ServiceResult(ok=False, message=error)

    stock_error = _check_stock(payload)
    if stock_error:
        _LOGGER.warning("Insufficient stock for outbound: %s", stock_error)
        return ServiceResult(ok=False, message=stock_error)

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
    saved = event_engine.record_event(event)
    if not saved:
        return ServiceResult(ok=False, message="출고를 저장하지 못했습니다. 로그를 확인해 주세요.")
    return ServiceResult(ok=True, message="출고가 등록되었습니다.", payload=saved)


def apply_move(payload):
    """이동 이벤트를 생성하고 기록한다."""
    error = validator.validate_move(payload)
    if error:
        _LOGGER.warning("Move validation failed: %s", error)
        return ServiceResult(ok=False, message=error)

    stock_error = _check_stock(payload, location_key="from_location")
    if stock_error:
        _LOGGER.warning("Insufficient stock for move: %s", stock_error)
        return ServiceResult(ok=False, message=stock_error)

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
    saved = event_engine.record_event(event)
    if not saved:
        return ServiceResult(ok=False, message="이동 내역을 저장하지 못했습니다. 로그를 확인해 주세요.")
    return ServiceResult(ok=True, message="재고 이동이 등록되었습니다.", payload=saved)


def apply_return(payload):
    """반품 이벤트를 생성하고 기록한다."""
    error = validator.validate_return(payload)
    if error:
        _LOGGER.warning("Return validation failed: %s", error)
        return ServiceResult(ok=False, message=error)

    return_type = payload.get("return_type", "CUSTOMER")
    reference_type = "RETURN_CUSTOMER" if return_type == "CUSTOMER" else "RETURN_SUPPLIER"
    if reference_type == "RETURN_SUPPLIER":
        stock_error = _check_stock(payload)
        if stock_error:
            _LOGGER.warning("Insufficient stock for supplier return: %s", stock_error)
            return ServiceResult(ok=False, message=stock_error)

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
    saved = event_engine.record_event(event)
    if not saved:
        return ServiceResult(ok=False, message="반품 내역을 저장하지 못했습니다. 로그를 확인해 주세요.")
    return ServiceResult(ok=True, message="반품이 등록되었습니다.", payload=saved)


def check_safety_stock(inventory, items):
    """안전 재고 부족 품목을 반환한다."""
    shortages = []
    item_map = {item.get("item_id"): item for item in items if item.get("item_id")}
    for item_id, item in item_map.items():
        safety = item.get("safety_stock", 0) or 0
        total = inventory.get(item_id, {}).get("total", 0)
        if total < safety:
            shortages.append(item_id)
    return shortages


def rebuild_inventory(events):
    """이벤트를 재생성하여 재고를 재구축한다."""
    return event_engine.replay_inventory(events)


def _check_stock(payload, location_key="location_id"):
    """출고/이동 가능 재고를 점검하고 부족 사유를 반환한다."""
    data = storage.load_all_data()
    inventory = event_engine.replay_inventory(data.get("events", []))
    item_id = payload.get("item_id")
    location = payload.get(location_key)
    requested = int(payload.get("quantity", 0) or 0)

    if not item_id:
        return "품목 ID가 비어 있습니다."
    if requested <= 0:
        return "수량은 1 이상이어야 합니다."

    entry = inventory.get(item_id, {})
    if location:
        available = entry.get("locations", {}).get(location, 0)
        if available < requested:
            return f"재고 부족: {item_id}/{location} 현재 {available}, 요청 {requested}"
        return ""

    available = entry.get("total", 0)
    if available < requested:
        return f"재고 부족: {item_id} 현재 {available}, 요청 {requested}"
    return ""
