import sys
from pathlib import Path
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from modules import inventory_service


class InventoryRuleTests(unittest.TestCase):
    def test_check_safety_stock_includes_items_without_inventory(self):
        inventory = {"ITEM-001": {"total": 5, "locations": {}, "unit": "EA"}}
        items = [
            {"item_id": "ITEM-001", "safety_stock": 10},
            {"item_id": "ITEM-002", "safety_stock": 3},
        ]

        shortages = inventory_service.check_safety_stock(inventory, items)

        self.assertEqual(set(shortages), {"ITEM-001", "ITEM-002"})


if __name__ == "__main__":
    unittest.main()
