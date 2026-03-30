"""
목적: event_engine의 record_event, reverse_event 함수를 스토리지 Mock으로 검증한다.
대상: modules/event_engine.py (record_event, reverse_event)
"""
import unittest
from unittest.mock import patch, MagicMock
from pathlib import Path

from modules import event_engine


class RecordEventTests(unittest.TestCase):
    """record_event 검증."""

    def _mock_storage(self, append_return=True):
        """append_json_list와 get_data_dir를 Mock으로 설정한다."""
        return (
            patch("modules.event_engine.storage.append_json_list", return_value=append_return),
            patch("modules.event_engine.get_data_dir", return_value=Path("/tmp/erp_test")),
        )

    def test_none_event_returns_none(self):
        result = event_engine.record_event(None)
        self.assertIsNone(result)

    def test_empty_dict_event_returns_none(self):
        """빈 dict는 falsy이므로 None을 반환해야 한다."""
        result = event_engine.record_event({})
        self.assertIsNone(result)

    def test_valid_event_returns_payload_with_event_id(self):
        event = {
            "event_type": "INBOUND",
            "item_id": "ITEM-A",
            "quantity": 5,
            "unit": "EA",
            "location_id": "LOC-1",
        }
        p1, p2 = self._mock_storage()
        with p1, p2:
            result = event_engine.record_event(event)
        self.assertIsNotNone(result)
        self.assertIn("event_id", result)
        self.assertEqual(result["event_type"], "INBOUND")
        self.assertEqual(result["item_id"], "ITEM-A")
        self.assertEqual(result["quantity"], 5)

    def test_existing_event_id_is_preserved(self):
        event = {
            "event_id": "MY-FIXED-ID",
            "event_type": "OUTBOUND",
            "item_id": "ITEM-B",
            "quantity": 2,
            "unit": "EA",
            "location_id": "LOC-2",
        }
        p1, p2 = self._mock_storage()
        with p1, p2:
            result = event_engine.record_event(event)
        self.assertEqual(result["event_id"], "MY-FIXED-ID")

    def test_storage_failure_returns_none(self):
        event = {
            "event_type": "INBOUND",
            "item_id": "ITEM-A",
            "quantity": 3,
            "unit": "EA",
            "location_id": "LOC-1",
        }
        p1, p2 = self._mock_storage(append_return=False)
        with p1, p2:
            result = event_engine.record_event(event)
        self.assertIsNone(result)

    def test_event_lines_are_appended(self):
        """event에 lines가 있으면 event_lines.json에도 append_json_list가 호출되어야 한다."""
        event = {
            "event_type": "INBOUND",
            "item_id": "ITEM-A",
            "quantity": 3,
            "unit": "EA",
            "location_id": "LOC-1",
            "lines": [{"sku": "SKU-1", "qty": 3}],
        }
        mock_append = MagicMock(return_value=True)
        with patch("modules.event_engine.storage.append_json_list", mock_append), \
             patch("modules.event_engine.get_data_dir", return_value=Path("/tmp")):
            event_engine.record_event(event)
        # 최소 2번 호출 (events.json + event_lines.json)
        self.assertGreaterEqual(mock_append.call_count, 2)

    def test_default_user_applied_when_created_by_absent(self):
        event = {
            "event_type": "INBOUND",
            "item_id": "ITEM-X",
            "quantity": 1,
            "unit": "EA",
            "location_id": "LOC-1",
        }
        p1, p2 = self._mock_storage()
        with p1, p2, patch("modules.event_engine.get_default_user", return_value="test_user"):
            result = event_engine.record_event(event)
        self.assertEqual(result["created_by"], "test_user")


class ReverseEventTests(unittest.TestCase):
    """reverse_event 검증."""

    def _mock_data(self, events):
        return patch("modules.event_engine.storage.load_all_data", return_value={"events": events})

    def test_no_events_returns_none(self):
        with self._mock_data([]):
            result = event_engine.reverse_event("EVT-1")
        self.assertIsNone(result)

    def test_target_not_found_returns_none(self):
        events = [{"event_id": "EVT-1", "event_type": "INBOUND", "item_id": "X",
                   "quantity": 1, "unit": "EA", "location_id": "L"}]
        with self._mock_data(events):
            result = event_engine.reverse_event("NONEXISTENT")
        self.assertIsNone(result)

    def test_already_reversed_returns_none(self):
        events = [
            {"event_id": "EVT-1", "event_type": "INBOUND", "item_id": "X",
             "quantity": 1, "unit": "EA", "location_id": "L"},
            {"event_id": "EVT-2", "event_type": "REVERSAL", "reverses_event_id": "EVT-1",
             "item_id": "X", "quantity": 1, "unit": "EA", "location_id": "L"},
        ]
        with self._mock_data(events):
            result = event_engine.reverse_event("EVT-1")
        self.assertIsNone(result)

    def test_valid_event_id_creates_reversal(self):
        events = [
            {"event_id": "EVT-1", "event_type": "INBOUND", "item_id": "ITEM-A",
             "quantity": 5, "unit": "EA", "location_id": "LOC-1",
             "reference_type": "NONE", "reference_id": None},
        ]
        with self._mock_data(events), \
             patch("modules.event_engine.storage.append_json_list", return_value=True), \
             patch("modules.event_engine.get_data_dir", return_value=Path("/tmp")):
            result = event_engine.reverse_event("EVT-1")
        self.assertIsNotNone(result)
        self.assertEqual(result["event_type"], "REVERSAL")
        self.assertEqual(result["reverses_event_id"], "EVT-1")
        self.assertEqual(result["item_id"], "ITEM-A")
        self.assertEqual(result["quantity"], 5)


if __name__ == "__main__":
    unittest.main()
