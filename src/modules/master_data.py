import logging
import os

from config import get_data_dir
from modules import storage

_LOGGER = logging.getLogger(__name__)


_PROFILE_DATA = {
    "general": {
        "items": [
            {"item_id": "ITEM-001", "item_name": "Standard Gloves", "category": "Medical", "unit": "BOX", "safety_stock": 20, "reorder_qty": 50},
            {"item_id": "ITEM-002", "item_name": "Cleaning Tissue", "category": "Consumable", "unit": "PACK", "safety_stock": 30, "reorder_qty": 100},
        ],
        "locations": [
            {"location_id": "LOC-001", "location_name": "Main Warehouse"},
            {"location_id": "LOC-002", "location_name": "Store Front"},
        ],
        "partners": [
            {"partner_id": "PARTNER-001", "partner_name": "Core Supplier", "type": "SUPPLIER"},
            {"partner_id": "PARTNER-002", "partner_name": "Walk-in Customer", "type": "CUSTOMER"},
        ],
    },
    "wholesale": {
        "items": [
            {"item_id": "W-CASE-001", "item_name": "Beverage Case", "category": "Food", "unit": "CASE", "safety_stock": 100, "reorder_qty": 200},
            {"item_id": "W-HOME-010", "item_name": "Home Cleaner", "category": "Household", "unit": "BOX", "safety_stock": 80, "reorder_qty": 160},
        ],
        "locations": [
            {"location_id": "WH-A", "location_name": "Bulk Warehouse A"},
            {"location_id": "WH-B", "location_name": "Bulk Warehouse B"},
        ],
        "partners": [
            {"partner_id": "SUP-100", "partner_name": "National Distributor", "type": "SUPPLIER"},
            {"partner_id": "CUS-100", "partner_name": "Regional Retailer", "type": "CUSTOMER"},
        ],
    },
    "retail": {
        "items": [
            {"item_id": "R-SNK-001", "item_name": "Snack Bar", "category": "Food", "unit": "EA", "safety_stock": 40, "reorder_qty": 120},
            {"item_id": "R-COS-002", "item_name": "Face Cream", "category": "Beauty", "unit": "EA", "safety_stock": 20, "reorder_qty": 60},
        ],
        "locations": [
            {"location_id": "STORE-01", "location_name": "Main Store"},
            {"location_id": "BACKROOM", "location_name": "Backroom"},
        ],
        "partners": [
            {"partner_id": "SUP-RET-01", "partner_name": "Retail Supplier", "type": "SUPPLIER"},
            {"partner_id": "MEMBER", "partner_name": "Member Customer", "type": "CUSTOMER"},
        ],
    },
    "ecommerce": {
        "items": [
            {"item_id": "E-ACC-101", "item_name": "Phone Case", "category": "Accessory", "unit": "EA", "safety_stock": 200, "reorder_qty": 500},
            {"item_id": "E-CBL-201", "item_name": "USB Cable", "category": "Accessory", "unit": "EA", "safety_stock": 300, "reorder_qty": 700},
        ],
        "locations": [
            {"location_id": "FC-SEOUL", "location_name": "Fulfillment Center"},
            {"location_id": "RET-AREA", "location_name": "Return Processing"},
        ],
        "partners": [
            {"partner_id": "SUP-EC-01", "partner_name": "Online Supplier", "type": "SUPPLIER"},
            {"partner_id": "MKT-01", "partner_name": "Marketplace", "type": "CUSTOMER"},
        ],
    },
    "hospital": {
        "items": [
            {"item_id": "H-MED-001", "item_name": "Syringe 5ml", "category": "Medical", "unit": "BOX", "safety_stock": 60, "reorder_qty": 150},
            {"item_id": "H-MED-002", "item_name": "N95 Mask", "category": "Medical", "unit": "BOX", "safety_stock": 100, "reorder_qty": 250},
        ],
        "locations": [
            {"location_id": "PHARM", "location_name": "Pharmacy"},
            {"location_id": "ER-STOCK", "location_name": "ER Stock"},
        ],
        "partners": [
            {"partner_id": "SUP-MED-01", "partner_name": "Medical Vendor", "type": "SUPPLIER"},
            {"partner_id": "PATIENT", "partner_name": "Patient", "type": "CUSTOMER"},
        ],
    },
}


def initialize_if_empty():
    """Seed master data for first run only."""
    profile = os.getenv("ERP_PROFILE", "general").strip().lower()
    if profile not in _PROFILE_DATA:
        _LOGGER.warning("Unknown ERP_PROFILE '%s', fallback to general", profile)
        profile = "general"
    dataset = _PROFILE_DATA[profile]
    data_dir = get_data_dir()

    for filename, key in (("items.json", "items"), ("locations.json", "locations"), ("partners.json", "partners")):
        path = data_dir / filename
        current = storage.load_json(path, [])
        if isinstance(current, list) and current:
            continue
        if not storage.save_json(path, dataset[key]):
            _LOGGER.error("Failed to initialize %s", filename)
