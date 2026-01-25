import logging
from pathlib import Path

from PySide6.QtCore import QFile
from PySide6.QtUiTools import QUiLoader
from PySide6.QtWidgets import (
    QDialog,
    QLabel,
    QLineEdit,
    QListWidget,
    QMessageBox,
    QPushButton,
    QSpinBox,
    QTableWidget,
    QTableWidgetItem,
    QComboBox,
)

from config import is_admin_mode
from modules import dashboard, event_engine, inventory_service, order_service, storage

_LOGGER = logging.getLogger(__name__)


class MainController:
    """
    역할: UI 이벤트 흐름 제어
    책임: 화면 이동, 입력 수집, 서비스 호출, UI 갱신
    외부 의존성: PySide6, UI .ui 파일, inventory/order/dashboard 모듈
    """

    def __init__(self, window):
        self.window = window
        self.data = storage.load_all_data()
        self.inventory = inventory_service.rebuild_inventory(self.data.get("events", []))
        self._connect_signals()

    def _connect_signals(self):
        """
        목적: UI 위젯 신호를 연결한다.
        Args:
            없음
        Returns:
            None
        Side Effects:
            UI 이벤트 핸들러 연결
        Raises:
            없음
        """
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

    def open_inbound_dialog(self):
        """
        목적: 입고 다이얼로그를 연다.
        Args:
            없음
        Returns:
            None
        Side Effects:
            다이얼로그 표시
        Raises:
            없음
        """
        dialog = self._load_dialog("inbound_dialog.ui")
        if self._run_dialog(dialog):
            data = self._collect_inbound(dialog)
            self.confirm_inbound(data)

    def open_outbound_dialog(self):
        """
        목적: 출고 다이얼로그를 연다.
        Args:
            없음
        Returns:
            None
        Side Effects:
            다이얼로그 표시
        Raises:
            없음
        """
        dialog = self._load_dialog("outbound_dialog.ui")
        if self._run_dialog(dialog):
            data = self._collect_outbound(dialog)
            self.confirm_outbound(data)

    def open_order_dialog(self):
        """
        목적: 발주 다이얼로그를 연다.
        Args:
            없음
        Returns:
            None
        Side Effects:
            다이얼로그 표시
        Raises:
            없음
        """
        dialog = self._load_dialog("order_dialog.ui")
        if self._run_dialog(dialog):
            data = self._collect_order(dialog)
            self.confirm_order(data)

    def open_return_dialog(self):
        """
        목적: 반품 다이얼로그를 연다.
        Args:
            없음
        Returns:
            None
        Side Effects:
            다이얼로그 표시
        Raises:
            없음
        """
        dialog = self._load_dialog("return_dialog.ui")
        if self._run_dialog(dialog):
            data = self._collect_return(dialog)
            self.confirm_return(data)

    def open_move_dialog(self):
        """
        목적: 이동 다이얼로그를 연다.
        Args:
            없음
        Returns:
            None
        Side Effects:
            다이얼로그 표시
        Raises:
            없음
        """
        dialog = self._load_dialog("move_dialog.ui")
        if self._run_dialog(dialog):
            data = self._collect_move(dialog)
            self.confirm_move(data)

    def confirm_inbound(self, data):
        """
        목적: 입고 확정을 처리한다.
        Args:
            data (dict): 입고 데이터
        Returns:
            None
        Side Effects:
            이벤트 기록 및 UI 갱신
        Raises:
            없음
        """
        result = inventory_service.apply_inbound(data)
        if not result:
            self._show_error("Inbound failed")
            return
        self._after_event("Inbound confirmed")

    def confirm_outbound(self, data):
        """
        목적: 출고 확정을 처리한다.
        Args:
            data (dict): 출고 데이터
        Returns:
            None
        Side Effects:
            이벤트 기록 및 UI 갱신
        Raises:
            없음
        """
        result = inventory_service.apply_outbound(data)
        if not result:
            self._show_error("Outbound failed")
            return
        self._after_event("Outbound confirmed")

    def confirm_order(self, data):
        """
        목적: 발주 확정을 처리한다.
        Args:
            data (dict): 발주 데이터
        Returns:
            None
        Side Effects:
            이벤트 기록 및 UI 갱신
        Raises:
            없음
        """
        result = order_service.create_order(data)
        if not result:
            self._show_error("Order failed")
            return
        self._after_event("Order confirmed")

    def confirm_return(self, data):
        """
        목적: 반품 확정을 처리한다.
        Args:
            data (dict): 반품 데이터
        Returns:
            None
        Side Effects:
            이벤트 기록 및 UI 갱신
        Raises:
            없음
        """
        result = inventory_service.apply_return(data)
        if not result:
            self._show_error("Return failed")
            return
        self._after_event("Return confirmed")

    def confirm_move(self, data):
        """
        목적: 이동 확정을 처리한다.
        Args:
            data (dict): 이동 데이터
        Returns:
            None
        Side Effects:
            이벤트 기록 및 UI 갱신
        Raises:
            없음
        """
        result = inventory_service.apply_move(data)
        if not result:
            self._show_error("Move failed")
            return
        self._after_event("Move confirmed")

    def undo_last_event(self):
        """
        목적: 마지막 이벤트를 되돌린다.
        Args:
            없음
        Returns:
            None
        Side Effects:
            이벤트 기록 및 UI 갱신
        Raises:
            없음
        """
        if not is_admin_mode():
            self._show_error("Admin mode required for undo")
            return
        events = self.data.get("events", [])
        target = next((event for event in reversed(events) if event.get("event_type") != "REVERSAL"), None)
        if not target:
            self._show_error("No event to undo")
            return
        reversed_event = event_engine.reverse_event(target.get("event_id"))
        if not reversed_event:
            self._show_error("Undo failed")
            return
        self._after_event("Undo confirmed")

    def refresh_inventory_table(self):
        """
        목적: 재고 테이블을 갱신한다.
        Args:
            없음
        Returns:
            None
        Side Effects:
            테이블 렌더링
        Raises:
            없음
        """
        self.data = storage.load_all_data()
        self.inventory = inventory_service.rebuild_inventory(self.data.get("events", []))
        table = self.window.inventoryTable
        if not isinstance(table, QTableWidget):
            return
        search_text = ""
        if self.window.searchLineEdit:
            search_text = self.window.searchLineEdit.text().strip().lower()
        table.clear()
        table.setColumnCount(5)
        table.setHorizontalHeaderLabels(["Item ID", "Total", "Unit", "Locations", "Safety"])
        items = self.data.get("items", [])
        shortages = inventory_service.check_safety_stock(self.inventory, items)
        rows = []
        for item_id, entry in self.inventory.items():
            if search_text and search_text not in item_id.lower():
                continue
            rows.append((item_id, entry))
        table.setRowCount(len(rows))
        for row_index, (item_id, entry) in enumerate(rows):
            locations = ", ".join(f"{loc}:{qty}" for loc, qty in entry.get("locations", {}).items())
            safety_text = "LOW" if item_id in shortages else "OK"
            table.setItem(row_index, 0, QTableWidgetItem(item_id))
            table.setItem(row_index, 1, QTableWidgetItem(str(entry.get("total", 0))))
            table.setItem(row_index, 2, QTableWidgetItem(str(entry.get("unit") or "")))
            table.setItem(row_index, 3, QTableWidgetItem(locations))
            table.setItem(row_index, 4, QTableWidgetItem(safety_text))
        if self.window.safetyBadgeLabel:
            self.window.safetyBadgeLabel.setText(f"Safety: {len(shortages)} items")
        if self.window.statusLabel:
            self.window.statusLabel.setText("Updated")

    def open_dashboard(self):
        """
        목적: 대시보드를 연다.
        Args:
            없음
        Returns:
            None
        Side Effects:
            다이얼로그 표시
        Raises:
            없음
        """
        dialog = self._load_dialog("dashboard_dialog.ui")
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

    def _after_event(self, message):
        """
        목적: 이벤트 처리 후 공통 동작을 수행한다.
        Args:
            message (str): 사용자 메시지
        Returns:
            None
        Side Effects:
            데이터 재로딩 및 UI 갱신
        Raises:
            없음
        """
        self.data = storage.load_all_data()
        self.inventory = inventory_service.rebuild_inventory(self.data.get("events", []))
        self.refresh_inventory_table()
        self._show_info(message)

    def _load_dialog(self, filename):
        """
        목적: 다이얼로그 UI를 로딩한다.
        Args:
            filename (str): UI 파일명
        Returns:
            QDialog: 로딩된 다이얼로그
        Side Effects:
            파일 접근
        Raises:
            없음
        """
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
        """
        목적: 다이얼로그의 확인/취소 버튼을 연결하고 실행한다.
        Args:
            dialog (QDialog): 다이얼로그
        Returns:
            bool: 확인 여부
        Side Effects:
            다이얼로그 표시
        Raises:
            없음
        """
        confirm = dialog.findChild(QPushButton, "confirmButton")
        cancel = dialog.findChild(QPushButton, "cancelButton")
        if confirm:
            confirm.clicked.connect(dialog.accept)
        if cancel:
            cancel.clicked.connect(dialog.reject)
        return dialog.exec() == QDialog.Accepted

    def _collect_inbound(self, dialog):
        """
        목적: 입고 다이얼로그 입력을 수집한다.
        Args:
            dialog (QDialog): 다이얼로그
        Returns:
            dict: 입력 데이터
        Side Effects:
            없음
        Raises:
            없음
        """
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
        """
        목적: 출고 다이얼로그 입력을 수집한다.
        Args:
            dialog (QDialog): 다이얼로그
        Returns:
            dict: 입력 데이터
        Side Effects:
            없음
        Raises:
            없음
        """
        return {
            "item_id": self._get_text(dialog, "itemIdLineEdit"),
            "quantity": self._get_spin(dialog, "quantitySpinBox"),
            "unit": self._get_text(dialog, "unitLineEdit"),
            "location_id": self._get_text(dialog, "locationLineEdit"),
            "reason": self._get_text(dialog, "reasonLineEdit"),
        }

    def _collect_order(self, dialog):
        """
        목적: 발주 다이얼로그 입력을 수집한다.
        Args:
            dialog (QDialog): 다이얼로그
        Returns:
            dict: 입력 데이터
        Side Effects:
            없음
        Raises:
            없음
        """
        return {
            "item_id": self._get_text(dialog, "itemIdLineEdit"),
            "quantity": self._get_spin(dialog, "quantitySpinBox"),
            "unit": self._get_text(dialog, "unitLineEdit"),
            "partner_id": self._get_text(dialog, "partnerLineEdit"),
            "reason": self._get_text(dialog, "reasonLineEdit"),
        }

    def _collect_return(self, dialog):
        """
        목적: 반품 다이얼로그 입력을 수집한다.
        Args:
            dialog (QDialog): 다이얼로그
        Returns:
            dict: 입력 데이터
        Side Effects:
            없음
        Raises:
            없음
        """
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
        """
        목적: 이동 다이얼로그 입력을 수집한다.
        Args:
            dialog (QDialog): 다이얼로그
        Returns:
            dict: 입력 데이터
        Side Effects:
            없음
        Raises:
            없음
        """
        return {
            "item_id": self._get_text(dialog, "itemIdLineEdit"),
            "quantity": self._get_spin(dialog, "quantitySpinBox"),
            "unit": self._get_text(dialog, "unitLineEdit"),
            "from_location": self._get_text(dialog, "fromLocationLineEdit"),
            "to_location": self._get_text(dialog, "toLocationLineEdit"),
            "reason": self._get_text(dialog, "reasonLineEdit"),
        }

    def _get_text(self, dialog, name):
        """
        목적: QLineEdit 텍스트를 반환한다.
        Args:
            dialog (QDialog): 다이얼로그
            name (str): 위젯 이름
        Returns:
            str: 입력값
        Side Effects:
            없음
        Raises:
            없음
        """
        widget = dialog.findChild(QLineEdit, name)
        return widget.text().strip() if widget else ""

    def _get_spin(self, dialog, name):
        """
        목적: QSpinBox 값을 반환한다.
        Args:
            dialog (QDialog): 다이얼로그
            name (str): 위젯 이름
        Returns:
            int: 입력값
        Side Effects:
            없음
        Raises:
            없음
        """
        widget = dialog.findChild(QSpinBox, name)
        return int(widget.value()) if widget else 0

    def _get_combo(self, dialog, name):
        """
        목적: QComboBox 선택 값을 반환한다.
        Args:
            dialog (QDialog): 다이얼로그
            name (str): 위젯 이름
        Returns:
            str: 선택값
        Side Effects:
            없음
        Raises:
            없음
        """
        widget = dialog.findChild(QComboBox, name)
        return widget.currentText().strip().upper() if widget else "CUSTOMER"

    def _set_label_text(self, dialog, name, value):
        """
        목적: QLabel 텍스트를 설정한다.
        Args:
            dialog (QDialog): 다이얼로그
            name (str): 위젯 이름
            value (str): 표시 텍스트
        Returns:
            None
        Side Effects:
            라벨 텍스트 변경
        Raises:
            없음
        """
        widget = dialog.findChild(QLabel, name)
        if widget:
            widget.setText(value)

    def _show_error(self, message):
        """
        목적: 사용자 오류 메시지를 표시한다.
        Args:
            message (str): 메시지
        Returns:
            None
        Side Effects:
            메시지 박스 표시
        Raises:
            없음
        """
        QMessageBox.warning(self.window, "Error", message)

    def _show_info(self, message):
        """
        목적: 사용자 안내 메시지를 표시한다.
        Args:
            message (str): 메시지
        Returns:
            None
        Side Effects:
            메시지 박스 표시
        Raises:
            없음
        """
        QMessageBox.information(self.window, "Info", message)
