import logging

from modules import event_engine, validator

_LOGGER = logging.getLogger(__name__)


def create_order(payload):
    """
    목적: 발주 이벤트를 생성하고 기록한다.
    Args:
        payload (dict): 발주 데이터
    Returns:
        dict|None: 기록된 이벤트
    Side Effects:
        events.json 쓰기
    Raises:
        없음
    """
    error = validator.validate_order(payload)
    if error:
        _LOGGER.warning("Order validation failed: %s", error)
        return None
    event = {
        "event_type": "ORDER",
        "item_id": payload["item_id"],
        "quantity": payload["quantity"],
        "unit": payload["unit"],
        "location_id": None,
        "reference_type": "ORDER",
        "reference_id": payload.get("partner_id"),
        "reason": payload.get("reason", ""),
    }
    return event_engine.record_event(event)


def link_inbound(order_id, inbound_event_id):
    """
    목적: 입고 이벤트와 발주 이벤트를 연결한다.
    Args:
        order_id (str): 발주 이벤트 ID
        inbound_event_id (str): 입고 이벤트 ID
    Returns:
        dict|None: 기록된 이벤트
    Side Effects:
        events.json 쓰기
    Raises:
        없음
    """
    event = {
        "event_type": "ORDER",
        "item_id": None,
        "quantity": 0,
        "unit": None,
        "location_id": None,
        "reference_type": "ORDER_LINK",
        "reference_id": f"{order_id}:{inbound_event_id}",
        "reason": "Link inbound",
    }
    return event_engine.record_event(event)


def close_order(order_id):
    """
    목적: 발주를 종료 처리한다.
    Args:
        order_id (str): 발주 이벤트 ID
    Returns:
        dict|None: 기록된 이벤트
    Side Effects:
        events.json 쓰기
    Raises:
        없음
    """
    event = {
        "event_type": "ORDER",
        "item_id": None,
        "quantity": 0,
        "unit": None,
        "location_id": None,
        "reference_type": "ORDER_CLOSE",
        "reference_id": order_id,
        "reason": "Close order",
    }
    return event_engine.record_event(event)
