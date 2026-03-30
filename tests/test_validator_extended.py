"""
목적: validator 모듈의 모든 검증 함수와 엣지 케이스를 검증한다.
대상: modules/validator.py
"""
import unittest

from modules import validator


class ValidateCommonNonDictTests(unittest.TestCase):
    """비 dict 페이로드 처리 검증."""

    def test_none_payload_returns_error(self):
        result = validator.validate_inbound(None)
        self.assertIsNotNone(result)
        self.assertIn("형식", result)

    def test_list_payload_returns_error(self):
        result = validator.validate_inbound([1, 2, 3])
        self.assertIsNotNone(result)

    def test_string_payload_returns_error(self):
        result = validator.validate_inbound("invalid")
        self.assertIsNotNone(result)


class ValidateInboundTests(unittest.TestCase):
    """validate_inbound 전체 경로 검증."""

    def _valid(self, **kwargs):
        base = {"item_id": "I1", "quantity": 1, "unit": "EA", "location_id": "L1"}
        base.update(kwargs)
        return base

    def test_valid_payload_returns_none(self):
        self.assertIsNone(validator.validate_inbound(self._valid()))

    def test_missing_unit_returns_error(self):
        error = validator.validate_inbound({"item_id": "I1", "quantity": 1, "location_id": "L1"})
        self.assertIn("단위", error)

    def test_missing_location_id_returns_error(self):
        error = validator.validate_inbound({"item_id": "I1", "quantity": 1, "unit": "EA"})
        self.assertIn("위치", error)

    def test_quantity_zero_returns_error(self):
        error = validator.validate_inbound(self._valid(quantity=0))
        self.assertIn("수량", error)

    def test_quantity_negative_returns_error(self):
        error = validator.validate_inbound(self._valid(quantity=-5))
        self.assertIn("수량", error)


class ValidateOutboundTests(unittest.TestCase):
    """validate_outbound 검증."""

    def test_valid_payload_returns_none(self):
        payload = {"item_id": "I1", "quantity": 1, "unit": "EA", "location_id": "L1"}
        self.assertIsNone(validator.validate_outbound(payload))

    def test_missing_item_id_returns_error(self):
        error = validator.validate_outbound({"quantity": 1, "unit": "EA", "location_id": "L1"})
        self.assertIn("품목 ID", error)


class ValidateMoveTests(unittest.TestCase):
    """validate_move 검증."""

    def _valid(self):
        return {"item_id": "I1", "quantity": 1, "unit": "EA",
                "from_location": "L1", "to_location": "L2"}

    def test_valid_payload_returns_none(self):
        self.assertIsNone(validator.validate_move(self._valid()))

    def test_missing_from_location_returns_error(self):
        payload = {"item_id": "I1", "quantity": 1, "unit": "EA", "to_location": "L2"}
        error = validator.validate_move(payload)
        self.assertIn("출발 위치", error)

    def test_missing_to_location_returns_error(self):
        payload = {"item_id": "I1", "quantity": 1, "unit": "EA", "from_location": "L1"}
        error = validator.validate_move(payload)
        self.assertIn("도착 위치", error)


class ValidateReturnTests(unittest.TestCase):
    """validate_return 엣지 케이스 검증."""

    def _valid(self, return_type="CUSTOMER"):
        return {"item_id": "I1", "quantity": 1, "unit": "EA",
                "location_id": "L1", "return_type": return_type}

    def test_customer_return_valid(self):
        self.assertIsNone(validator.validate_return(self._valid("CUSTOMER")))

    def test_supplier_return_valid(self):
        self.assertIsNone(validator.validate_return(self._valid("SUPPLIER")))

    def test_missing_return_type_returns_error(self):
        payload = {"item_id": "I1", "quantity": 1, "unit": "EA", "location_id": "L1"}
        error = validator.validate_return(payload)
        self.assertIn("반품 유형", error)

    def test_invalid_return_type_none_returns_error(self):
        payload = {**self._valid(), "return_type": None}
        error = validator.validate_return(payload)
        self.assertIn("반품 유형", error)

    def test_common_validation_runs_first(self):
        """공통 검증이 먼저 실행되어 quantity 오류가 반품유형 오류보다 먼저 나와야 한다."""
        payload = {"item_id": "I1", "quantity": 0, "unit": "EA",
                   "location_id": "L1", "return_type": "CUSTOMER"}
        error = validator.validate_return(payload)
        self.assertIn("수량", error)


class ValidateOrderTests(unittest.TestCase):
    """validate_order 검증."""

    def _valid(self):
        return {"item_id": "I1", "quantity": 2, "unit": "EA", "partner_id": "P1"}

    def test_valid_payload_returns_none(self):
        self.assertIsNone(validator.validate_order(self._valid()))

    def test_missing_partner_id_returns_error(self):
        payload = {"item_id": "I1", "quantity": 2, "unit": "EA"}
        error = validator.validate_order(payload)
        self.assertIn("거래처", error)

    def test_missing_item_id_returns_error(self):
        payload = {"quantity": 2, "unit": "EA", "partner_id": "P1"}
        error = validator.validate_order(payload)
        self.assertIn("품목 ID", error)

    def test_zero_quantity_returns_error(self):
        error = validator.validate_order({**self._valid(), "quantity": 0})
        self.assertIn("수량", error)


if __name__ == "__main__":
    unittest.main()
