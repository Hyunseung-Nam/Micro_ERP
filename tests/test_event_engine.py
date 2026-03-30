"""
목적: event_engine 모듈의 replay_inventory 및 _apply_event 로직을 검증한다.
대상: modules/event_engine.py
"""
import unittest

from modules import event_engine


def _make_event(event_type, item_id="ITEM-A", quantity=10, location_id="LOC-1",
                reference_type=None, reference_id=None, event_id=None,
                reverses_event_id=None):
    """테스트용 이벤트 딕셔너리를 생성하는 헬퍼."""
    e = {
        "event_id": event_id or f"EVT-{event_type}-001",
        "event_type": event_type,
        "item_id": item_id,
        "quantity": quantity,
        "unit": "EA",
        "location_id": location_id,
        "reference_type": reference_type or "NONE",
        "reference_id": reference_id,
    }
    if reverses_event_id:
        e["reverses_event_id"] = reverses_event_id
    return e


class ReplayInventoryInboundTests(unittest.TestCase):
    """INBOUND 이벤트 재생 검증."""

    def test_empty_events_returns_empty_inventory(self):
        result = event_engine.replay_inventory([])
        self.assertEqual(result, {})

    def test_single_inbound_adds_to_total_and_location(self):
        events = [_make_event("INBOUND", quantity=5, location_id="LOC-1")]
        inventory = event_engine.replay_inventory(events)
        self.assertEqual(inventory["ITEM-A"]["total"], 5)
        self.assertEqual(inventory["ITEM-A"]["locations"]["LOC-1"], 5)

    def test_multiple_inbounds_accumulate(self):
        events = [
            _make_event("INBOUND", quantity=3, location_id="LOC-1", event_id="E1"),
            _make_event("INBOUND", quantity=7, location_id="LOC-1", event_id="E2"),
        ]
        inventory = event_engine.replay_inventory(events)
        self.assertEqual(inventory["ITEM-A"]["total"], 10)
        self.assertEqual(inventory["ITEM-A"]["locations"]["LOC-1"], 10)

    def test_inbound_across_multiple_locations(self):
        events = [
            _make_event("INBOUND", quantity=4, location_id="LOC-1", event_id="E1"),
            _make_event("INBOUND", quantity=6, location_id="LOC-2", event_id="E2"),
        ]
        inventory = event_engine.replay_inventory(events)
        self.assertEqual(inventory["ITEM-A"]["total"], 10)
        self.assertEqual(inventory["ITEM-A"]["locations"]["LOC-1"], 4)
        self.assertEqual(inventory["ITEM-A"]["locations"]["LOC-2"], 6)


class ReplayInventoryOutboundTests(unittest.TestCase):
    """OUTBOUND 이벤트 재생 검증."""

    def test_outbound_subtracts_from_total_and_location(self):
        events = [
            _make_event("INBOUND", quantity=10, location_id="LOC-1", event_id="E1"),
            _make_event("OUTBOUND", quantity=3, location_id="LOC-1", event_id="E2"),
        ]
        inventory = event_engine.replay_inventory(events)
        self.assertEqual(inventory["ITEM-A"]["total"], 7)
        self.assertEqual(inventory["ITEM-A"]["locations"]["LOC-1"], 7)

    def test_outbound_only_results_in_negative_total(self):
        events = [_make_event("OUTBOUND", quantity=5, location_id="LOC-1")]
        inventory = event_engine.replay_inventory(events)
        self.assertEqual(inventory["ITEM-A"]["total"], -5)


class ReplayInventoryMoveTests(unittest.TestCase):
    """MOVE 이벤트 재생 검증."""

    def test_move_transfers_between_locations(self):
        events = [
            _make_event("INBOUND", quantity=10, location_id="LOC-1", event_id="E1"),
            {
                "event_id": "E2",
                "event_type": "MOVE",
                "item_id": "ITEM-A",
                "quantity": 4,
                "unit": "EA",
                "location_id": "LOC-2",      # to_location
                "reference_id": "LOC-1",      # from_location
                "reference_type": "MOVE",
            },
        ]
        inventory = event_engine.replay_inventory(events)
        self.assertEqual(inventory["ITEM-A"]["total"], 10)  # total 변화 없음
        self.assertEqual(inventory["ITEM-A"]["locations"]["LOC-1"], 6)
        self.assertEqual(inventory["ITEM-A"]["locations"]["LOC-2"], 4)

    def test_move_without_from_location_uses_unspecified(self):
        events = [
            {
                "event_id": "E1",
                "event_type": "MOVE",
                "item_id": "ITEM-A",
                "quantity": 3,
                "unit": "EA",
                "location_id": "LOC-2",
                "reference_id": None,
                "reference_type": "MOVE",
            }
        ]
        inventory = event_engine.replay_inventory(events)
        self.assertIn("UNSPECIFIED", inventory["ITEM-A"]["locations"])
        self.assertEqual(inventory["ITEM-A"]["locations"]["UNSPECIFIED"], -3)
        self.assertEqual(inventory["ITEM-A"]["locations"]["LOC-2"], 3)


class ReplayInventoryReturnTests(unittest.TestCase):
    """RETURN 이벤트 재생 검증."""

    def test_customer_return_increases_inventory(self):
        events = [
            _make_event("RETURN", quantity=2, location_id="LOC-1",
                        reference_type="RETURN_CUSTOMER")
        ]
        inventory = event_engine.replay_inventory(events)
        self.assertEqual(inventory["ITEM-A"]["total"], 2)
        self.assertEqual(inventory["ITEM-A"]["locations"]["LOC-1"], 2)

    def test_supplier_return_decreases_inventory(self):
        events = [
            _make_event("INBOUND", quantity=10, location_id="LOC-1", event_id="E1"),
            _make_event("RETURN", quantity=3, location_id="LOC-1",
                        reference_type="RETURN_SUPPLIER", event_id="E2"),
        ]
        inventory = event_engine.replay_inventory(events)
        self.assertEqual(inventory["ITEM-A"]["total"], 7)
        self.assertEqual(inventory["ITEM-A"]["locations"]["LOC-1"], 7)


class ReplayInventoryReversalTests(unittest.TestCase):
    """REVERSAL 이벤트 재생 검증."""

    def test_reversal_undoes_inbound(self):
        events = [
            _make_event("INBOUND", quantity=10, location_id="LOC-1", event_id="E1"),
            {
                "event_id": "E2",
                "event_type": "REVERSAL",
                "item_id": "ITEM-A",
                "quantity": 10,
                "unit": "EA",
                "location_id": "LOC-1",
                "reference_type": "NONE",
                "reference_id": None,
                "reverses_event_id": "E1",
            },
        ]
        inventory = event_engine.replay_inventory(events)
        self.assertEqual(inventory["ITEM-A"]["total"], 0)
        self.assertEqual(inventory["ITEM-A"]["locations"]["LOC-1"], 0)

    def test_reversal_with_missing_original_is_ignored(self):
        events = [
            {
                "event_id": "E2",
                "event_type": "REVERSAL",
                "item_id": "ITEM-A",
                "quantity": 5,
                "unit": "EA",
                "location_id": "LOC-1",
                "reference_type": "NONE",
                "reference_id": None,
                "reverses_event_id": "NONEXISTENT",
            }
        ]
        # 원본이 없으면 아무 변화도 없어야 한다
        inventory = event_engine.replay_inventory(events)
        self.assertEqual(inventory, {})

    def test_reversal_partially_reverts_sequence(self):
        events = [
            _make_event("INBOUND", quantity=10, location_id="LOC-1", event_id="E1"),
            _make_event("INBOUND", quantity=5, location_id="LOC-1", event_id="E2"),
            {
                "event_id": "E3",
                "event_type": "REVERSAL",
                "item_id": "ITEM-A",
                "quantity": 10,
                "unit": "EA",
                "location_id": "LOC-1",
                "reference_type": "NONE",
                "reference_id": None,
                "reverses_event_id": "E1",
            },
        ]
        inventory = event_engine.replay_inventory(events)
        self.assertEqual(inventory["ITEM-A"]["total"], 5)


class ReplayInventoryOrderSkipTests(unittest.TestCase):
    """ORDER 이벤트는 재고 계산에서 무시되어야 한다."""

    def test_order_event_is_ignored(self):
        events = [
            {
                "event_id": "E1",
                "event_type": "ORDER",
                "item_id": "ITEM-A",
                "quantity": 100,
                "unit": "EA",
                "location_id": "LOC-1",
                "reference_type": "NONE",
                "reference_id": None,
            }
        ]
        inventory = event_engine.replay_inventory(events)
        self.assertEqual(inventory, {})


class ReplayInventoryMultiItemTests(unittest.TestCase):
    """여러 품목을 동시에 처리하는 시나리오 검증."""

    def test_multiple_items_independent(self):
        events = [
            {**_make_event("INBOUND", item_id="A", quantity=10, event_id="E1"), "item_id": "A"},
            {**_make_event("INBOUND", item_id="B", quantity=20, event_id="E2"), "item_id": "B"},
            {**_make_event("OUTBOUND", item_id="A", quantity=3, event_id="E3"), "item_id": "A"},
        ]
        inventory = event_engine.replay_inventory(events)
        self.assertEqual(inventory["A"]["total"], 7)
        self.assertEqual(inventory["B"]["total"], 20)

    def test_event_without_item_id_is_skipped(self):
        events = [
            {"event_id": "E1", "event_type": "INBOUND", "item_id": None,
             "quantity": 5, "unit": "EA", "location_id": "LOC-1"}
        ]
        inventory = event_engine.replay_inventory(events)
        self.assertEqual(inventory, {})


if __name__ == "__main__":
    unittest.main()
