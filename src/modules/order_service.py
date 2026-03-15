import logging

from modules import event_engine, validator
from modules.service_result import ServiceResult

_LOGGER = logging.getLogger(__name__)


def create_order(payload):
    """발주 이벤트를 생성하고 기록한다."""
    error = validator.validate_order(payload)
    if error:
        _LOGGER.warning("Order validation failed: %s", error)
        return ServiceResult(ok=False, message=error)

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
    saved = event_engine.record_event(event)
    if not saved:
        return ServiceResult(ok=False, message="발주를 저장하지 못했습니다. 로그를 확인해 주세요.")
    return ServiceResult(ok=True, message="발주가 등록되었습니다.", payload=saved)


def link_inbound(order_id, inbound_event_id):
    """입고 이벤트와 발주 이벤트를 연결한다."""
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
    saved = event_engine.record_event(event)
    if not saved:
        return ServiceResult(ok=False, message="발주 연결을 저장하지 못했습니다.")
    return ServiceResult(ok=True, payload=saved)


def close_order(order_id):
    """발주를 종료 처리한다."""
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
    saved = event_engine.record_event(event)
    if not saved:
        return ServiceResult(ok=False, message="발주 종료를 저장하지 못했습니다.")
    return ServiceResult(ok=True, payload=saved)
