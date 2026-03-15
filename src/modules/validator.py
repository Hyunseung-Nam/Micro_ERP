import logging

_LOGGER = logging.getLogger(__name__)


class ValidationError(Exception):
    """
    역할: 입력 검증 실패를 표현
    책임: 검증 오류 타입 식별
    외부 의존성: 없음
    """


def validate_inbound(payload):
    """
    목적: 입고 입력을 검증한다.
    Args:
        payload (dict): 입력 데이터
    Returns:
        str|None: 오류 메시지 또는 None
    Side Effects:
        없음
    Raises:
        없음
    """
    return _validate_common(payload, required_fields=("item_id", "quantity", "unit", "location_id"))


def validate_outbound(payload):
    """
    목적: 출고 입력을 검증한다.
    Args:
        payload (dict): 입력 데이터
    Returns:
        str|None: 오류 메시지 또는 None
    Side Effects:
        없음
    Raises:
        없음
    """
    return _validate_common(payload, required_fields=("item_id", "quantity", "unit", "location_id"))


def validate_move(payload):
    """
    목적: 이동 입력을 검증한다.
    Args:
        payload (dict): 입력 데이터
    Returns:
        str|None: 오류 메시지 또는 None
    Side Effects:
        없음
    Raises:
        없음
    """
    return _validate_common(
        payload,
        required_fields=("item_id", "quantity", "unit", "from_location", "to_location"),
    )


def validate_return(payload):
    """
    목적: 반품 입력을 검증한다.
    Args:
        payload (dict): 입력 데이터
    Returns:
        str|None: 오류 메시지 또는 None
    Side Effects:
        없음
    Raises:
        없음
    """
    error = _validate_common(payload, required_fields=("item_id", "quantity", "unit", "location_id"))
    if error:
        return error
    return_type = payload.get("return_type")
    if return_type not in {"CUSTOMER", "SUPPLIER"}:
        return "반품 유형은 CUSTOMER 또는 SUPPLIER 여야 합니다."
    return None


def validate_order(payload):
    """
    목적: 발주 입력을 검증한다.
    Args:
        payload (dict): 입력 데이터
    Returns:
        str|None: 오류 메시지 또는 None
    Side Effects:
        없음
    Raises:
        없음
    """
    return _validate_common(payload, required_fields=("item_id", "quantity", "unit", "partner_id"))


def _validate_common(payload, required_fields):
    """
    목적: 공통 입력 필드를 검증한다.
    Args:
        payload (dict): 입력 데이터
        required_fields (tuple): 필수 필드 목록
    Returns:
        str|None: 오류 메시지 또는 None
    Side Effects:
        없음
    Raises:
        없음
    """
    if not isinstance(payload, dict):
        _LOGGER.warning("Payload is not dict")
        return "입력 데이터 형식이 올바르지 않습니다."

    field_labels = {
        "item_id": "품목 ID",
        "quantity": "수량",
        "unit": "단위",
        "location_id": "위치",
        "from_location": "출발 위치",
        "to_location": "도착 위치",
        "partner_id": "거래처",
    }

    for field in required_fields:
        value = payload.get(field)
        if value is None or value == "":
            return f"{field_labels.get(field, field)} 값을 입력해 주세요."
    quantity = payload.get("quantity", 0)
    if quantity <= 0:
        return "수량은 1 이상이어야 합니다."
    return None
