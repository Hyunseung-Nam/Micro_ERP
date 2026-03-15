import sys
from pathlib import Path
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from modules import validator


class ValidatorMessageTests(unittest.TestCase):
    def test_missing_item_id_message(self):
        error = validator.validate_inbound({"quantity": 1, "unit": "EA", "location_id": "LOC-1"})
        self.assertIn("품목 ID", error)

    def test_invalid_return_type_message(self):
        error = validator.validate_return(
            {
                "item_id": "ITEM-1",
                "quantity": 1,
                "unit": "EA",
                "location_id": "LOC-1",
                "return_type": "BAD",
            }
        )
        self.assertIn("반품 유형", error)


if __name__ == "__main__":
    unittest.main()
