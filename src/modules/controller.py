import logging
from datetime import datetime
from pathlib import Path

from PySide6.QtCore import QFile, Qt
from PySide6.QtGui import QColor
from PySide6.QtUiTools import QUiLoader
from PySide6.QtWidgets import (
    QComboBox,
    QDialog,
    QInputDialog,
    QLabel,
    QLineEdit,
    QListWidget,
    QMessageBox,
    QPushButton,
    QSpinBox,
    QTableWidget,
    QTableWidgetItem,
)

from config import is_admin_mode
from modules import dashboard, event_engine, inventory_service, order_service, storage
from modules.api_client import ApiClient

_LOGGER = logging.getLogger(__name__)


class MainController:
    """UI 이벤트 흐름 제어."""

    def __init__(self, window):
        self.window = window
        self.api_client = ApiClient()
        self.use_api = self.api_client.enabled
        self.data = storage.load_all_data()
        self.inventory = inventory_service.rebuild_inventory(self.data.get("events", []))
        self._connect_signals()
        if self.use_api:
            self._bootstrap_api_session()
        self.refresh_inventory_table()

    def _connect_signals(self):
        if self.window.inboundButton:
            self.window.inboundButton.clicked.connect(self.open_inbound_dialog)
        if self.window.outboundButton:
            self.window.outboundButton.clicked.connect(self.open_outbound_dialog)
        if self.window.orderButton:
            self.window.orderButton.clicked.connect(self.open_order_dialog)
        if self.window.returnButton:
            self.window.returnButton.clicked.connect(self.open_return_dialog)
        if self.window.moveButton:
            self.window.moveButton.clicked.connect(self.open_move_dialog)
        if self.window.dashboardButton:
            self.window.dashboardButton.clicked.connect(self.open_dashboard)
        if self.window.undoButton:
            self.window.undoButton.clicked.connect(self.undo_last_event)
        if self.window.refreshButton:
            self.window.refreshButton.clicked.connect(self.refresh_inventory_table)
        if self.window.searchLineEdit:
            self.window.searchLineEdit.textChanged.connect(self.refresh_inventory_table)
        if getattr(self.window, "approvalButton", None):
            self.window.approvalButton.clicked.connect(self.open_approval_dialog)
        if getattr(self.window, "workflowButton", None):
            self.window.workflowButton.clicked.connect(self.open_workflow_dialog)

    def _bootstrap_api_session(self):
        username, ok = QInputDialog.getText(self.window, "API Login", "Username:", text="admin")
        if not ok:
            self.use_api = False
            self._show_info("API 모드를 취소했습니다. 로컬 모드로 동작합니다.")
            return

        password, ok = QInputDialog.getText(self.window, "API Login", "Password:", QLineEdit.Password, "admin123")
        if not ok:
            self.use_api = False
            self._show_info("API 모드를 취소했습니다. 로컬 모드로 동작합니다.")
            return

        login = self.api_client.login(username.strip(), password)
        if not login.ok:
            self.use_api = False
            self._show_error(f"API 로그인 실패: {login.message}\n로컬 모드로 전환합니다.")
            return

        if getattr(self.window, "userInfoLabel", None):
            role = self.api_client.current_role or "UNKNOWN"
            self.window.userInfoLabel.setText(f"User: {self.api_client.current_user} ({role})")

    def open_inbound_dialog(self):
        dialog = self._load_dialog("inbound_dialog.ui")
        self._prefill_dialog(dialog, include_partner=True, include_location=True, include_unit=True)
        if self._run_dialog(dialog):
            data = self._collect_inbound(dialog)
            self.confirm_inbound(data)

    def open_outbound_dialog(self):
        dialog = self._load_dialog("outbound_dialog.ui")
        self._prefill_dialog(dialog, include_location=True, include_unit=True)
        if self._run_dialog(dialog):
            data = self._collect_outbound(dialog)
            self.confirm_outbound(data)

    def open_order_dialog(self):
        dialog = self._load_dialog("order_dialog.ui")
        self._prefill_dialog(dialog, include_partner=True, include_unit=True)
        if self._run_dialog(dialog):
            data = self._collect_order(dialog)
            self.confirm_order(data)

    def open_return_dialog(self):
        dialog = self._load_dialog("return_dialog.ui")
        self._prefill_dialog(dialog, include_partner=True, include_location=True, include_unit=True)
        if self._run_dialog(dialog):
            data = self._collect_return(dialog)
            self.confirm_return(data)

    def open_move_dialog(self):
        dialog = self._load_dialog("move_dialog.ui")
        self._prefill_dialog(dialog, include_location=True, include_unit=True)
        self._prefill_move_locations(dialog)
        if self._run_dialog(dialog):
            data = self._collect_move(dialog)
            self.confirm_move(data)

    def confirm_inbound(self, data):
        if self.use_api:
            result = self.api_client.adjust_inventory(data["item_id"], data["location_id"], data["quantity"])
            if not result.ok:
                self._show_error(result.message)
                return
            self._show_info("입고가 API 서버에 반영되었습니다.")
            self.refresh_inventory_table()
            return

        result = inventory_service.apply_inbound(data)
        self._handle_result(result)

    def confirm_outbound(self, data):
        if self.use_api:
            result = self.api_client.adjust_inventory(data["item_id"], data["location_id"], -data["quantity"])
            if not result.ok:
                self._show_error(result.message)
                return
            self._show_info("출고가 API 서버에 반영되었습니다.")
            self.refresh_inventory_table()
            return

        result = inventory_service.apply_outbound(data)
        self._handle_result(result)

    def confirm_order(self, data):
        if self.use_api:
            result = self.api_client.create_order(
                partner_id=data["partner_id"],
                item_id=data["item_id"],
                quantity=data["quantity"],
                unit=data["unit"],
            )
            if not result.ok:
                self._show_error(result.message)
                return
            order_id = result.payload.get("orderId", "")
            self._show_info(f"발주가 생성되었습니다. orderId={order_id}")
            return

        result = order_service.create_order(data)
        self._handle_result(result)

    def confirm_return(self, data):
        if self.use_api:
            delta = data["quantity"] if data.get("return_type") == "CUSTOMER" else -data["quantity"]
            result = self.api_client.adjust_inventory(data["item_id"], data["location_id"], delta)
            if not result.ok:
                self._show_error(result.message)
                return
            self._show_info("반품 처리가 API 서버에 반영되었습니다.")
            self.refresh_inventory_table()
            return

        result = inventory_service.apply_return(data)
        self._handle_result(result)

    def confirm_move(self, data):
        if self.use_api:
            out_result = self.api_client.adjust_inventory(data["item_id"], data["from_location"], -data["quantity"])
            if not out_result.ok:
                self._show_error(out_result.message)
                return
            in_result = self.api_client.adjust_inventory(data["item_id"], data["to_location"], data["quantity"])
            if not in_result.ok:
                self._show_error(in_result.message)
                return
            self._show_info("재고 이동이 API 서버에 반영되었습니다.")
            self.refresh_inventory_table()
            return

        result = inventory_service.apply_move(data)
        self._handle_result(result)

    def undo_last_event(self):
        if self.use_api:
            self._show_error("API 모드에서는 감사 추적 보존을 위해 되돌리기를 지원하지 않습니다.")
            return
        if not is_admin_mode():
            self._show_error("관리자 모드에서만 되돌리기를 사용할 수 있습니다.")
            return

        events = self.data.get("events", [])
        target = next((event for event in reversed(events) if event.get("event_type") != "REVERSAL"), None)
        if not target:
            self._show_error("되돌릴 이벤트가 없습니다.")
            return

        reversed_event = event_engine.reverse_event(target.get("event_id"))
        if not reversed_event:
            self._show_error("되돌리기에 실패했습니다. 이미 되돌린 내역일 수 있습니다.")
            return
        self._after_event("마지막 이벤트를 되돌렸습니다.")

    def refresh_inventory_table(self):
        if self.use_api:
            self._refresh_inventory_from_api()
            return

        self.data = storage.load_all_data()
        self.inventory = inventory_service.rebuild_inventory(self.data.get("events", []))
        self._render_inventory_table(self.inventory, self.data.get("items", []))

    def _refresh_inventory_from_api(self):
        response = self.api_client.get_inventory()
        if not response.ok:
            self._show_error(response.message)
            return

        rows = response.payload if isinstance(response.payload, list) else []
        grouped = {}
        items = {}
        for row in rows:
            item_id = row.get("itemId", "")
            if not item_id:
                continue
            entry = grouped.setdefault(item_id, {"total": 0, "locations": {}, "unit": row.get("unit", "")})
            qty = int(row.get("quantity", 0) or 0)
            loc = row.get("locationId", "UNSPECIFIED")
            entry["total"] += qty
            entry["locations"][loc] = qty
            items[item_id] = {
                "item_id": item_id,
                "item_name": row.get("itemName", ""),
                "category": "-",
                "unit": row.get("unit", ""),
                "safety_stock": int(row.get("safetyStock", 0) or 0),
                "reorder_qty": max(int(row.get("safetyStock", 0) or 0) * 2, 1),
            }

        self.inventory = grouped
        self.data["items"] = list(items.values())
        self._render_inventory_table(self.inventory, self.data.get("items", []))

    def _render_inventory_table(self, inventory, items):
        table = self.window.inventoryTable
        if not isinstance(table, QTableWidget):
            return

        search_text = ""
        if self.window.searchLineEdit:
            search_text = self.window.searchLineEdit.text().strip().lower()

        item_map = {item.get("item_id"): item for item in items if item.get("item_id")}
        shortages = set(inventory_service.check_safety_stock(inventory, items))

        merged_ids = sorted(set(item_map.keys()) | set(inventory.keys()))
        rows = []
        for item_id in merged_ids:
            entry = inventory.get(item_id, {"total": 0, "locations": {}, "unit": ""})
            meta = item_map.get(item_id, {})
            item_name = meta.get("item_name", "")
            category = meta.get("category", "")
            locations = ", ".join(
                f"{loc}:{qty}" for loc, qty in sorted(entry.get("locations", {}).items()) if qty != 0
            ) or "-"
            safety = int(meta.get("safety_stock", 0) or 0)
            total = int(entry.get("total", 0) or 0)
            reorder_qty = int(meta.get("reorder_qty", 0) or 0)
            recommended = max(safety - total, 0)
            if recommended == 0 and total < safety and reorder_qty > 0:
                recommended = reorder_qty

            searchable = " ".join([item_id, item_name, category, locations]).lower()
            if search_text and search_text not in searchable:
                continue

            rows.append(
                {
                    "item_id": item_id,
                    "item_name": item_name or "-",
                    "category": category or "-",
                    "total": total,
                    "unit": entry.get("unit") or meta.get("unit") or "-",
                    "safety": safety,
                    "recommended": recommended,
                    "locations": locations,
                    "is_low": item_id in shortages,
                }
            )

        table.clear()
        table.setColumnCount(8)
        table.setHorizontalHeaderLabels(["품목 ID", "품목명", "카테고리", "현재고", "단위", "안전재고", "권장발주", "위치별 재고"])
        table.setRowCount(len(rows))

        for row_index, row in enumerate(rows):
            self._set_table_item(table, row_index, 0, row["item_id"])
            self._set_table_item(table, row_index, 1, row["item_name"])
            self._set_table_item(table, row_index, 2, row["category"])
            self._set_table_item(table, row_index, 3, str(row["total"]))
            self._set_table_item(table, row_index, 4, str(row["unit"]))
            self._set_table_item(table, row_index, 5, str(row["safety"]))
            self._set_table_item(table, row_index, 6, str(row["recommended"]))
            self._set_table_item(table, row_index, 7, row["locations"])

            if row["is_low"]:
                for column in range(8):
                    item = table.item(row_index, column)
                    if item:
                        item.setBackground(QColor("#ffe8e8"))

        if self.window.safetyBadgeLabel:
            self.window.safetyBadgeLabel.setText(f"안전재고 부족: {len(shortages)}건")
        if self.window.statusLabel:
            now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            source = "API" if self.use_api else "LOCAL"
            self.window.statusLabel.setText(f"{source} | 총 {len(rows)}개 품목 | 마지막 갱신 {now}")

    def open_dashboard(self):
        dialog = self._load_dialog("dashboard_dialog.ui")
        if self.use_api:
            self._set_label_text(dialog, "totalInboundLabel", "API mode")
            self._set_label_text(dialog, "totalOutboundLabel", "Use audit logs")
            self._set_label_text(dialog, "totalReturnLabel", "Use workflow")
            self._set_label_text(dialog, "netChangeLabel", "Use BI/report")
            self._run_dialog(dialog)
            return

        data = dashboard.build_monthly_dashboard(self.data.get("events", []))
        self._set_label_text(dialog, "totalInboundLabel", str(data["total_inbound"]))
        self._set_label_text(dialog, "totalOutboundLabel", str(data["total_outbound"]))
        self._set_label_text(dialog, "totalReturnLabel", str(data["total_return"]))
        self._set_label_text(dialog, "netChangeLabel", str(data["net_change"]))

        shortage_list = dialog.findChild(QListWidget, "shortageList")
        top_list = dialog.findChild(QListWidget, "topTurnoverList")
        if shortage_list:
            shortage_list.clear()
            shortages = dashboard.shortage_items(self.inventory, self.data.get("items", []))
            for item_id in shortages:
                shortage_list.addItem(item_id)
        if top_list:
            top_list.clear()
            for item_id, score in dashboard.top_turnover_items(self.data.get("events", [])):
                top_list.addItem(f"{item_id}: {score}")
        self._run_dialog(dialog)

    def open_approval_dialog(self):
        if not self.use_api:
            self._show_info("로컬 모드에서는 승인함을 사용할 수 없습니다.")
            return

        action, ok = QInputDialog.getItem(self.window, "Approval", "Action", ["List Pending", "Approve", "Reject", "Request Adjust"], 0, False)
        if not ok:
            return

        if action == "List Pending":
            result = self.api_client.list_approvals("PENDING")
            if not result.ok:
                self._show_error(result.message)
                return
            payload = result.payload if isinstance(result.payload, list) else []
            if not payload:
                self._show_info("대기 중인 승인 요청이 없습니다.")
                return
            lines = [f"#{row.get('approvalId')} {row.get('requestType')} by {row.get('requestedBy')}" for row in payload]
            self._show_info("\n".join(lines))
            return

        if action in {"Approve", "Reject"}:
            approval_id, ok = QInputDialog.getInt(self.window, "Approval", "Approval ID", 1, 1)
            if not ok:
                return
            if action == "Approve":
                result = self.api_client.approve(approval_id)
            else:
                reason, ok = QInputDialog.getText(self.window, "Reject", "Reason")
                if not ok:
                    return
                result = self.api_client.reject(approval_id, reason)
            if not result.ok:
                self._show_error(result.message)
                return
            self._show_info(f"승인 요청 {approval_id} 처리 완료")
            self.refresh_inventory_table()
            return

        item_id, ok = QInputDialog.getText(self.window, "Approval Request", "Item ID")
        if not ok:
            return
        location_id, ok = QInputDialog.getText(self.window, "Approval Request", "Location ID")
        if not ok:
            return
        delta, ok = QInputDialog.getInt(self.window, "Approval Request", "Delta Quantity", 0, -1000000, 1000000)
        if not ok:
            return
        reason, ok = QInputDialog.getText(self.window, "Approval Request", "Reason")
        if not ok:
            return

        result = self.api_client.create_approval(
            "INVENTORY_ADJUST",
            {
                "itemId": item_id.strip(),
                "locationId": location_id.strip(),
                "deltaQuantity": int(delta),
                "reason": reason.strip(),
            },
        )
        if not result.ok:
            self._show_error(result.message)
            return
        approval_id = (result.payload or {}).get("approvalId", "")
        self._show_info(f"승인 요청이 등록되었습니다. approvalId={approval_id}")

    def open_workflow_dialog(self):
        if not self.use_api:
            self._show_info("업종 워크플로우는 API 모드에서 동작합니다.")
            return

        workflow, ok = QInputDialog.getItem(
            self.window,
            "Industry Workflow",
            "Workflow",
            ["Hospital Consume", "Ecommerce Return/Exchange"],
            0,
            False,
        )
        if not ok:
            return

        if workflow == "Hospital Consume":
            item_id, ok = QInputDialog.getText(self.window, "Hospital", "Item ID")
            if not ok:
                return
            location_id, ok = QInputDialog.getText(self.window, "Hospital", "Location ID")
            if not ok:
                return
            quantity, ok = QInputDialog.getInt(self.window, "Hospital", "Quantity", 1, 1)
            if not ok:
                return
            department, ok = QInputDialog.getText(self.window, "Hospital", "Department", text="ER")
            if not ok:
                return
            note, ok = QInputDialog.getText(self.window, "Hospital", "Note")
            if not ok:
                return

            result = self.api_client.hospital_consume(item_id, location_id, quantity, department, note)
            if not result.ok:
                self._show_error(result.message)
                return
            self._show_info("병원 사용량 차감이 반영되었습니다.")
            self.refresh_inventory_table()
            return

        item_id, ok = QInputDialog.getText(self.window, "Ecommerce", "Item ID")
        if not ok:
            return
        return_location, ok = QInputDialog.getText(self.window, "Ecommerce", "Return Location ID")
        if not ok:
            return
        ship_location, ok = QInputDialog.getText(self.window, "Ecommerce", "Ship Location ID")
        if not ok:
            return
        return_qty, ok = QInputDialog.getInt(self.window, "Ecommerce", "Return Quantity", 1, 1)
        if not ok:
            return
        exchange_qty, ok = QInputDialog.getInt(self.window, "Ecommerce", "Exchange Quantity", 0, 0)
        if not ok:
            return
        order_no, ok = QInputDialog.getText(self.window, "Ecommerce", "Marketplace Order No")
        if not ok:
            return

        result = self.api_client.ecommerce_return_exchange(
            item_id,
            return_location,
            ship_location,
            return_qty,
            exchange_qty,
            order_no,
        )
        if not result.ok:
            self._show_error(result.message)
            return
        self._show_info("쇼핑몰 반품/교환 처리가 반영되었습니다.")
        self.refresh_inventory_table()

    def _set_table_item(self, table, row, column, value):
        item = QTableWidgetItem(value)
        if column in {3, 5, 6}:
            item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
        table.setItem(row, column, item)

    def _handle_result(self, result):
        if not result or not result.ok:
            self._show_error(result.message if result else "작업에 실패했습니다.")
            return
        self._after_event(result.message or "작업이 완료되었습니다.")

    def _after_event(self, message):
        self.data = storage.load_all_data()
        self.inventory = inventory_service.rebuild_inventory(self.data.get("events", []))
        self.refresh_inventory_table()
        self._show_info(message)

    def _load_dialog(self, filename):
        ui_path = Path(__file__).resolve().parent.parent / "ui" / "dialogs" / filename
        loader = QUiLoader()
        file = QFile(str(ui_path))
        try:
            if not file.open(QFile.ReadOnly):
                _LOGGER.error("Dialog open failed: %s", ui_path)
                return QDialog()
            widget = loader.load(file)
            if widget is None:
                _LOGGER.error("Dialog load failed: %s", ui_path)
                return QDialog()
        finally:
            file.close()

        if isinstance(widget, QDialog):
            return widget
        dialog = QDialog()
        dialog.setLayout(widget.layout())
        return dialog

    def _run_dialog(self, dialog):
        confirm = dialog.findChild(QPushButton, "confirmButton")
        cancel = dialog.findChild(QPushButton, "cancelButton")
        if confirm:
            confirm.clicked.connect(dialog.accept)
        if cancel:
            cancel.clicked.connect(dialog.reject)
        return dialog.exec() == QDialog.Accepted

    def _prefill_dialog(self, dialog, include_partner=False, include_location=False, include_unit=False):
        items = self.data.get("items", [])
        partners = self.data.get("partners", [])
        locations = self.data.get("locations", [])

        if items:
            first_item = items[0]
            self._set_text_if_empty(dialog, "itemIdLineEdit", first_item.get("item_id", ""))
            if include_unit:
                self._set_text_if_empty(dialog, "unitLineEdit", first_item.get("unit", ""))

        if include_partner and partners:
            self._set_text_if_empty(dialog, "partnerLineEdit", partners[0].get("partner_id", ""))

        if include_location and locations:
            self._set_text_if_empty(dialog, "locationLineEdit", locations[0].get("location_id", ""))

    def _prefill_move_locations(self, dialog):
        locations = self.data.get("locations", [])
        if len(locations) >= 1:
            self._set_text_if_empty(dialog, "fromLocationLineEdit", locations[0].get("location_id", ""))
        if len(locations) >= 2:
            self._set_text_if_empty(dialog, "toLocationLineEdit", locations[1].get("location_id", ""))

    def _set_text_if_empty(self, dialog, widget_name, value):
        if not value:
            return
        widget = dialog.findChild(QLineEdit, widget_name)
        if widget and not widget.text().strip():
            widget.setText(value)

    def _collect_inbound(self, dialog):
        return {
            "item_id": self._get_text(dialog, "itemIdLineEdit"),
            "quantity": self._get_spin(dialog, "quantitySpinBox"),
            "unit": self._get_text(dialog, "unitLineEdit"),
            "location_id": self._get_text(dialog, "locationLineEdit"),
            "partner_id": self._get_text(dialog, "partnerLineEdit"),
            "order_id": self._get_text(dialog, "orderIdLineEdit"),
            "reason": self._get_text(dialog, "reasonLineEdit"),
        }

    def _collect_outbound(self, dialog):
        return {
            "item_id": self._get_text(dialog, "itemIdLineEdit"),
            "quantity": self._get_spin(dialog, "quantitySpinBox"),
            "unit": self._get_text(dialog, "unitLineEdit"),
            "location_id": self._get_text(dialog, "locationLineEdit"),
            "reason": self._get_text(dialog, "reasonLineEdit"),
        }

    def _collect_order(self, dialog):
        return {
            "item_id": self._get_text(dialog, "itemIdLineEdit"),
            "quantity": self._get_spin(dialog, "quantitySpinBox"),
            "unit": self._get_text(dialog, "unitLineEdit"),
            "partner_id": self._get_text(dialog, "partnerLineEdit"),
            "reason": self._get_text(dialog, "reasonLineEdit"),
        }

    def _collect_return(self, dialog):
        return_type = self._get_combo(dialog, "returnTypeComboBox")
        return {
            "item_id": self._get_text(dialog, "itemIdLineEdit"),
            "quantity": self._get_spin(dialog, "quantitySpinBox"),
            "unit": self._get_text(dialog, "unitLineEdit"),
            "return_type": return_type,
            "location_id": self._get_text(dialog, "locationLineEdit"),
            "partner_id": self._get_text(dialog, "partnerLineEdit"),
            "reason": self._get_text(dialog, "reasonLineEdit"),
        }

    def _collect_move(self, dialog):
        return {
            "item_id": self._get_text(dialog, "itemIdLineEdit"),
            "quantity": self._get_spin(dialog, "quantitySpinBox"),
            "unit": self._get_text(dialog, "unitLineEdit"),
            "from_location": self._get_text(dialog, "fromLocationLineEdit"),
            "to_location": self._get_text(dialog, "toLocationLineEdit"),
            "reason": self._get_text(dialog, "reasonLineEdit"),
        }

    def _get_text(self, dialog, name):
        widget = dialog.findChild(QLineEdit, name)
        return widget.text().strip() if widget else ""

    def _get_spin(self, dialog, name):
        widget = dialog.findChild(QSpinBox, name)
        return int(widget.value()) if widget else 0

    def _get_combo(self, dialog, name):
        widget = dialog.findChild(QComboBox, name)
        return widget.currentText().strip().upper() if widget else "CUSTOMER"

    def _set_label_text(self, dialog, name, value):
        widget = dialog.findChild(QLabel, name)
        if widget:
            widget.setText(value)

    def _show_error(self, message):
        QMessageBox.warning(self.window, "오류", message)

    def _show_info(self, message):
        QMessageBox.information(self.window, "안내", message)
