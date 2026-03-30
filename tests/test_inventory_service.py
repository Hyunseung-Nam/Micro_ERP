"""
목적: inventory_service 모듈의 apply_inbound, apply_outbound, apply_move,
      apply_return, check_safety_stock 로직을 검증한다.
대상: modules/inventory_service.py
"""
import unittest
from unittest.mock import patch, MagicMock

from modules import inventory_service


# ---------------------------------------------------------------------------
# 공통 유효 페이로드 헬퍼
# ---------------------------------------------------------------------------

def _inbound_payload(**kwargs):
    base = {"item_id": "ITEM-A", "quantity": 5, "unit": "EA", "location_id": "LOC-1"}
    base.update(kwargs)
    return base


def _outbound_payload(**kwargs):
    base = {"item_id": "ITEM-A", "quantity": 3, "unit": "EA", "location_id": "LOC-1"}
    base.update(kwargs)
    return base


def _move_payload(**kwargs):
    base = {
        "item_id": "ITEM-A", "quantity": 2, "unit": "EA",
        "from_location": "LOC-1", "to_location": "LOC-2",
    }
    base.update(kwargs)
    return base


def _return_payload(**kwargs):
    base = {
        "item_id": "ITEM-A", "quantity": 1, "unit": "EA",
        "location_id": "LOC-1", "return_type": "CUSTOMER",
    }
    base.update(kwargs)
    return base


# ---------------------------------------------------------------------------
# apply_inbound
# ---------------------------------------------------------------------------

class ApplyInboundTests(unittest.TestCase):
    """apply_inbound 검증."""

    @patch("modules.inventory_service.event_engine.record_event")
    def test_valid_payload_returns_ok(self, mock_record):
        """유효한 입고 페이로드 → ok=True."""
        mock_record.return_value = {"event_id": "E1"}
        result = inventory_service.apply_inbound(_inbound_payload())
        self.assertTrue(result.ok)
        self.assertIn("입고", result.message)

    @patch("modules.inventory_service.event_engine.record_event")
    def test_payload_with_order_id_sets_reference_type_order(self, mock_record):
        """order_id가 있으면 reference_type이 ORDER여야 한다."""
        mock_record.return_value = {"event_id": "E1"}
        inventory_service.apply_inbound(_inbound_payload(order_id="ORD-1"))
        called_event = mock_record.call_args[0][0]
        self.assertEqual(called_event["reference_type"], "ORDER")
        self.assertEqual(called_event["reference_id"], "ORD-1")

    @patch("modules.inventory_service.event_engine.record_event")
    def test_payload_without_order_id_sets_reference_type_none(self, mock_record):
        """order_id가 없으면 reference_type이 NONE이어야 한다."""
        mock_record.return_value = {"event_id": "E1"}
        inventory_service.apply_inbound(_inbound_payload())
        called_event = mock_record.call_args[0][0]
        self.assertEqual(called_event["reference_type"], "NONE")

    def test_missing_item_id_returns_error(self):
        """item_id 누락 → ok=False."""
        result = inventory_service.apply_inbound({"quantity": 5, "unit": "EA", "location_id": "LOC-1"})
        self.assertFalse(result.ok)
        self.assertIn("품목 ID", result.message)

    def test_zero_quantity_returns_error(self):
        """수량 0 → ok=False."""
        result = inventory_service.apply_inbound(_inbound_payload(quantity=0))
        self.assertFalse(result.ok)

    def test_negative_quantity_returns_error(self):
        """음수 수량 → ok=False."""
        result = inventory_service.apply_inbound(_inbound_payload(quantity=-1))
        self.assertFalse(result.ok)

    @patch("modules.inventory_service.event_engine.record_event", return_value=None)
    def test_record_event_failure_returns_error(self, _mock):
        """record_event가 None을 반환하면 ok=False."""
        result = inventory_service.apply_inbound(_inbound_payload())
        self.assertFalse(result.ok)
        self.assertIn("저장", result.message)


# ---------------------------------------------------------------------------
# apply_outbound
# ---------------------------------------------------------------------------

class ApplyOutboundTests(unittest.TestCase):
    """apply_outbound 검증."""

    def _stub_sufficient_stock(self, events=None, inventory=None):
        """충분한 재고가 있는 상태를 Mock으로 설정한다."""
        if inventory is None:
            inventory = {"ITEM-A": {"total": 100, "locations": {"LOC-1": 100}}}
        return (
            patch("modules.inventory_service.storage.load_all_data",
                  return_value={"events": events or []}),
            patch("modules.inventory_service.event_engine.replay_inventory",
                  return_value=inventory),
        )

    @patch("modules.inventory_service.event_engine.record_event")
    def test_valid_payload_with_sufficient_stock_returns_ok(self, mock_record):
        """재고 충분 + 유효 페이로드 → ok=True."""
        mock_record.return_value = {"event_id": "E1"}
        with patch("modules.inventory_service.storage.load_all_data", return_value={"events": []}), \
             patch("modules.inventory_service.event_engine.replay_inventory",
                   return_value={"ITEM-A": {"total": 100, "locations": {"LOC-1": 100}}}):
            result = inventory_service.apply_outbound(_outbound_payload())
        self.assertTrue(result.ok)
        self.assertIn("출고", result.message)

    def test_missing_item_id_returns_error(self):
        """item_id 누락 → ok=False (검증 단계에서 차단)."""
        result = inventory_service.apply_outbound({"quantity": 3, "unit": "EA", "location_id": "LOC-1"})
        self.assertFalse(result.ok)

    def test_insufficient_stock_returns_error(self):
        """재고 부족 → ok=False."""
        with patch("modules.inventory_service.storage.load_all_data", return_value={"events": []}), \
             patch("modules.inventory_service.event_engine.replay_inventory",
                   return_value={"ITEM-A": {"total": 1, "locations": {"LOC-1": 1}}}):
            result = inventory_service.apply_outbound(_outbound_payload(quantity=50))
        self.assertFalse(result.ok)
        self.assertIn("재고 부족", result.message)

    @patch("modules.inventory_service.event_engine.record_event", return_value=None)
    def test_record_event_failure_returns_error(self, _mock):
        """record_event 실패 → ok=False."""
        with patch("modules.inventory_service.storage.load_all_data", return_value={"events": []}), \
             patch("modules.inventory_service.event_engine.replay_inventory",
                   return_value={"ITEM-A": {"total": 100, "locations": {"LOC-1": 100}}}):
            result = inventory_service.apply_outbound(_outbound_payload())
        self.assertFalse(result.ok)


# ---------------------------------------------------------------------------
# apply_move
# ---------------------------------------------------------------------------

class ApplyMoveTests(unittest.TestCase):
    """apply_move 검증."""

    @patch("modules.inventory_service.event_engine.record_event")
    def test_valid_move_returns_ok(self, mock_record):
        """유효한 이동 요청 → ok=True."""
        mock_record.return_value = {"event_id": "E1"}
        with patch("modules.inventory_service.storage.load_all_data", return_value={"events": []}), \
             patch("modules.inventory_service.event_engine.replay_inventory",
                   return_value={"ITEM-A": {"total": 10, "locations": {"LOC-1": 10}}}):
            result = inventory_service.apply_move(_move_payload())
        self.assertTrue(result.ok)
        self.assertIn("이동", result.message)

    def test_missing_from_location_returns_error(self):
        """from_location 누락 → ok=False."""
        result = inventory_service.apply_move(
            {"item_id": "ITEM-A", "quantity": 2, "unit": "EA", "to_location": "LOC-2"}
        )
        self.assertFalse(result.ok)

    def test_insufficient_stock_in_from_location_returns_error(self):
        """출발 위치 재고 부족 → ok=False."""
        with patch("modules.inventory_service.storage.load_all_data", return_value={"events": []}), \
             patch("modules.inventory_service.event_engine.replay_inventory",
                   return_value={"ITEM-A": {"total": 1, "locations": {"LOC-1": 1}}}):
            result = inventory_service.apply_move(_move_payload(quantity=99))
        self.assertFalse(result.ok)
        self.assertIn("재고 부족", result.message)


# ---------------------------------------------------------------------------
# apply_return
# ---------------------------------------------------------------------------

class ApplyReturnTests(unittest.TestCase):
    """apply_return 검증."""

    @patch("modules.inventory_service.event_engine.record_event")
    def test_customer_return_returns_ok(self, mock_record):
        """고객 반품(CUSTOMER) → ok=True, 재고 체크 없음."""
        mock_record.return_value = {"event_id": "E1"}
        result = inventory_service.apply_return(_return_payload(return_type="CUSTOMER"))
        self.assertTrue(result.ok)
        self.assertIn("반품", result.message)

    @patch("modules.inventory_service.event_engine.record_event")
    def test_supplier_return_with_sufficient_stock_returns_ok(self, mock_record):
        """공급사 반품(SUPPLIER) + 재고 충분 → ok=True."""
        mock_record.return_value = {"event_id": "E1"}
        with patch("modules.inventory_service.storage.load_all_data", return_value={"events": []}), \
             patch("modules.inventory_service.event_engine.replay_inventory",
                   return_value={"ITEM-A": {"total": 100, "locations": {"LOC-1": 100}}}):
            result = inventory_service.apply_return(_return_payload(return_type="SUPPLIER"))
        self.assertTrue(result.ok)

    def test_supplier_return_with_insufficient_stock_returns_error(self):
        """공급사 반품(SUPPLIER) + 재고 부족 → ok=False."""
        with patch("modules.inventory_service.storage.load_all_data", return_value={"events": []}), \
             patch("modules.inventory_service.event_engine.replay_inventory",
                   return_value={"ITEM-A": {"total": 0, "locations": {"LOC-1": 0}}}):
            result = inventory_service.apply_return(_return_payload(return_type="SUPPLIER", quantity=5))
        self.assertFalse(result.ok)

    def test_invalid_return_type_returns_error(self):
        """잘못된 return_type → ok=False."""
        result = inventory_service.apply_return(_return_payload(return_type="INVALID"))
        self.assertFalse(result.ok)
        self.assertIn("반품 유형", result.message)


# ---------------------------------------------------------------------------
# check_safety_stock
# ---------------------------------------------------------------------------

class CheckSafetyStockTests(unittest.TestCase):
    """check_safety_stock 검증."""

    def test_no_shortage_returns_empty_list(self):
        inventory = {"ITEM-A": {"total": 20}}
        items = [{"item_id": "ITEM-A", "safety_stock": 10}]
        self.assertEqual(inventory_service.check_safety_stock(inventory, items), [])

    def test_item_below_safety_stock_included(self):
        inventory = {"ITEM-A": {"total": 5}}
        items = [{"item_id": "ITEM-A", "safety_stock": 10}]
        shortages = inventory_service.check_safety_stock(inventory, items)
        self.assertIn("ITEM-A", shortages)

    def test_item_not_in_inventory_treated_as_zero(self):
        inventory = {}
        items = [{"item_id": "ITEM-B", "safety_stock": 1}]
        shortages = inventory_service.check_safety_stock(inventory, items)
        self.assertIn("ITEM-B", shortages)

    def test_item_with_zero_safety_stock_never_shortage(self):
        inventory = {"ITEM-C": {"total": 0}}
        items = [{"item_id": "ITEM-C", "safety_stock": 0}]
        self.assertEqual(inventory_service.check_safety_stock(inventory, items), [])

    def test_items_without_item_id_are_ignored(self):
        inventory = {}
        items = [{"safety_stock": 5}]  # item_id 없음
        self.assertEqual(inventory_service.check_safety_stock(inventory, items), [])

    def test_multiple_items_mixed_results(self):
        inventory = {
            "ITEM-A": {"total": 15},
            "ITEM-B": {"total": 2},
        }
        items = [
            {"item_id": "ITEM-A", "safety_stock": 10},
            {"item_id": "ITEM-B", "safety_stock": 5},
            {"item_id": "ITEM-C", "safety_stock": 3},
        ]
        shortages = inventory_service.check_safety_stock(inventory, items)
        self.assertNotIn("ITEM-A", shortages)
        self.assertIn("ITEM-B", shortages)
        self.assertIn("ITEM-C", shortages)


if __name__ == "__main__":
    unittest.main()
