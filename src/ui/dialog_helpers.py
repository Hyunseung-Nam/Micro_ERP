"""
다이얼로그 로딩·스타일·프리필·폼 수집·액션/폼 다이얼로그 공통 로직.
Controller와 분리하여 확장성·유지보수성을 높인다.
"""

import logging
from pathlib import Path

from PySide6.QtCore import QFile
from PySide6.QtUiTools import QUiLoader
from PySide6.QtWidgets import (
    QComboBox,
    QDialog,
    QDialogButtonBox,
    QDoubleSpinBox,
    QFormLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QSpinBox,
    QVBoxLayout,
)

_LOGGER = logging.getLogger(__name__)

DIALOG_STYLESHEET = """
QDialog { background: #f4f6f8; color: #1c1f23; }
QLabel { color: #334155; font-size: 12px; }
QLineEdit, QSpinBox, QComboBox {
    background: #ffffff;
    border: 1px solid #cfd8e3;
    border-radius: 8px;
    min-height: 34px;
    padding: 4px 8px;
}
QPushButton {
    background: #ffffff;
    border: 1px solid #c9d1d9;
    border-radius: 8px;
    min-height: 34px;
    padding: 6px 12px;
    font-weight: 600;
}
QPushButton:hover { background: #eef4fa; }
"""

HINT_STYLESHEET = (
    "background:#eef4fb; border:1px solid #d5e3f5; border-radius:8px; padding:8px; color:#2d4a6b;"
)


class DialogHelper:
    """다이얼로그 공통 처리: 로딩, 스타일, 프리필, 값 수집, 액션/폼 다이얼로그."""

    def __init__(self, parent_window, dialogs_base_path, get_data):
        """
        Args:
            parent_window: 부모 윈도우 (QWidget)
            dialogs_base_path: .ui 파일이 있는 디렉터리 (Path)
            get_data: callable() -> dict with keys items, partners, locations
        """
        self.parent_window = parent_window
        self.dialogs_base_path = Path(dialogs_base_path)
        self.get_data = get_data

    def load_dialog(self, filename):
        """UI 파일을 로딩해 다이얼로그 위젯을 반환한다."""
        ui_path = self.dialogs_base_path / filename
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
            self.apply_dialog_style(widget)
            widget.resize(640, 420)
            return widget
        dialog = QDialog()
        dialog.setLayout(widget.layout())
        self.apply_dialog_style(dialog)
        dialog.resize(640, 420)
        return dialog

    def apply_dialog_style(self, dialog):
        dialog.setStyleSheet(DIALOG_STYLESHEET)

    def attach_dialog_hint(self, dialog, text):
        if dialog.findChild(QLabel, "hintLabel"):
            return
        layout = dialog.layout()
        if not layout:
            return
        hint = QLabel(text)
        hint.setObjectName("hintLabel")
        hint.setWordWrap(True)
        hint.setStyleSheet(HINT_STYLESHEET)
        layout.insertWidget(0, hint)

    def run_dialog(self, dialog):
        confirm = dialog.findChild(QPushButton, "confirmButton")
        cancel = dialog.findChild(QPushButton, "cancelButton")
        if confirm:
            confirm.clicked.connect(dialog.accept)
        if cancel:
            cancel.clicked.connect(dialog.reject)
        return dialog.exec() == QDialog.Accepted

    def prefill_dialog(self, dialog, include_partner=False, include_location=False, include_unit=False):
        data = self.get_data()
        items = data.get("items", [])
        partners = data.get("partners", [])
        locations = data.get("locations", [])

        if items:
            first_item = items[0]
            self.set_text_if_empty(dialog, "itemIdLineEdit", first_item.get("item_id", ""))
            if include_unit:
                self.set_text_if_empty(dialog, "unitLineEdit", first_item.get("unit", ""))

        if include_partner and partners:
            self.set_text_if_empty(dialog, "partnerLineEdit", partners[0].get("partner_id", ""))

        if include_location and locations:
            self.set_text_if_empty(dialog, "locationLineEdit", locations[0].get("location_id", ""))

    def prefill_move_locations(self, dialog):
        locations = self.get_data().get("locations", [])
        if len(locations) >= 1:
            self.set_text_if_empty(dialog, "fromLocationLineEdit", locations[0].get("location_id", ""))
        if len(locations) >= 2:
            self.set_text_if_empty(dialog, "toLocationLineEdit", locations[1].get("location_id", ""))

    def set_text_if_empty(self, dialog, widget_name, value):
        if not value:
            return
        widget = dialog.findChild(QLineEdit, widget_name)
        if widget and not widget.text().strip():
            widget.setText(value)

    def get_text(self, dialog, name):
        widget = dialog.findChild(QLineEdit, name)
        return widget.text().strip() if widget else ""

    def get_spin(self, dialog, name):
        widget = dialog.findChild(QSpinBox, name)
        return int(widget.value()) if widget else 0

    def get_combo(self, dialog, name):
        widget = dialog.findChild(QComboBox, name)
        if not widget:
            return "CUSTOMER"
        selected = widget.currentText().strip().upper()
        if selected in {"고객", "CUSTOMER"}:
            return "CUSTOMER"
        if selected in {"공급처", "SUPPLIER"}:
            return "SUPPLIER"
        return "CUSTOMER"

    def set_label_text(self, dialog, name, value):
        widget = dialog.findChild(QLabel, name)
        if widget:
            widget.setText(value)

    def collect_inbound(self, dialog):
        return {
            "item_id": self.get_text(dialog, "itemIdLineEdit"),
            "quantity": self.get_spin(dialog, "quantitySpinBox"),
            "unit": self.get_text(dialog, "unitLineEdit"),
            "location_id": self.get_text(dialog, "locationLineEdit"),
            "partner_id": self.get_text(dialog, "partnerLineEdit"),
            "order_id": self.get_text(dialog, "orderIdLineEdit"),
            "reason": self.get_text(dialog, "reasonLineEdit"),
        }

    def collect_outbound(self, dialog):
        return {
            "item_id": self.get_text(dialog, "itemIdLineEdit"),
            "quantity": self.get_spin(dialog, "quantitySpinBox"),
            "unit": self.get_text(dialog, "unitLineEdit"),
            "location_id": self.get_text(dialog, "locationLineEdit"),
            "reason": self.get_text(dialog, "reasonLineEdit"),
        }

    def collect_order(self, dialog):
        return {
            "item_id": self.get_text(dialog, "itemIdLineEdit"),
            "quantity": self.get_spin(dialog, "quantitySpinBox"),
            "unit": self.get_text(dialog, "unitLineEdit"),
            "partner_id": self.get_text(dialog, "partnerLineEdit"),
            "reason": self.get_text(dialog, "reasonLineEdit"),
        }

    def collect_return(self, dialog):
        return_type = self.get_combo(dialog, "returnTypeComboBox")
        return {
            "item_id": self.get_text(dialog, "itemIdLineEdit"),
            "quantity": self.get_spin(dialog, "quantitySpinBox"),
            "unit": self.get_text(dialog, "unitLineEdit"),
            "return_type": return_type,
            "location_id": self.get_text(dialog, "locationLineEdit"),
            "partner_id": self.get_text(dialog, "partnerLineEdit"),
            "reason": self.get_text(dialog, "reasonLineEdit"),
        }

    def collect_move(self, dialog):
        return {
            "item_id": self.get_text(dialog, "itemIdLineEdit"),
            "quantity": self.get_spin(dialog, "quantitySpinBox"),
            "unit": self.get_text(dialog, "unitLineEdit"),
            "from_location": self.get_text(dialog, "fromLocationLineEdit"),
            "to_location": self.get_text(dialog, "toLocationLineEdit"),
            "reason": self.get_text(dialog, "reasonLineEdit"),
        }

    def show_compact_action_dialog(self, title, help_text, actions):
        dialog = QDialog(self.parent_window)
        dialog.setWindowTitle(title)
        dialog.setModal(True)
        dialog.resize(520, 250)
        self.apply_dialog_style(dialog)

        layout = QVBoxLayout(dialog)
        helper = QLabel(help_text)
        helper.setWordWrap(True)
        layout.addWidget(helper)

        combo = QComboBox()
        combo.addItems(actions)
        layout.addWidget(combo)

        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        ok_btn = buttons.button(QDialogButtonBox.Ok)
        cancel_btn = buttons.button(QDialogButtonBox.Cancel)
        if ok_btn:
            ok_btn.setText("다음")
        if cancel_btn:
            cancel_btn.setText("취소")
        buttons.accepted.connect(dialog.accept)
        buttons.rejected.connect(dialog.reject)
        layout.addWidget(buttons)

        if dialog.exec() != QDialog.Accepted:
            return ""
        return combo.currentText().strip()

    def show_form_dialog(self, title, help_text, fields, submit_label="확인"):
        dialog = QDialog(self.parent_window)
        dialog.setWindowTitle(title)
        dialog.setModal(True)
        dialog.resize(640, 420)
        self.apply_dialog_style(dialog)

        layout = QVBoxLayout(dialog)
        helper = QLabel(help_text)
        helper.setWordWrap(True)
        layout.addWidget(helper)

        form_layout = QFormLayout()
        widgets = {}
        for field in fields:
            name = field["name"]
            label = field["label"]
            field_type = field.get("type", "text")
            default = field.get("default", "")
            if field_type == "int":
                widget = QSpinBox()
                widget.setRange(-1000000, 1000000)
                widget.setValue(int(default))
            elif field_type == "float":
                widget = QDoubleSpinBox()
                widget.setRange(-1000000.0, 1000000.0)
                widget.setValue(float(default))
            else:
                widget = QLineEdit()
                widget.setText(str(default))
            widgets[name] = widget
            form_layout.addRow(label, widget)
        layout.addLayout(form_layout)

        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        ok_btn = buttons.button(QDialogButtonBox.Ok)
        cancel_btn = buttons.button(QDialogButtonBox.Cancel)
        if ok_btn:
            ok_btn.setText(submit_label)
        if cancel_btn:
            cancel_btn.setText("취소")
        buttons.accepted.connect(dialog.accept)
        buttons.rejected.connect(dialog.reject)
        layout.addWidget(buttons)

        if dialog.exec() != QDialog.Accepted:
            return {}

        result = {}
        for name, widget in widgets.items():
            if isinstance(widget, (QSpinBox, QDoubleSpinBox)):
                result[name] = widget.value()
            else:
                result[name] = widget.text().strip()
        return result
