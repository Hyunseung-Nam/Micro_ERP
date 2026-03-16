import logging
from pathlib import Path

from PySide6.QtCore import QFile, Qt
from PySide6.QtGui import QFont
from PySide6.QtUiTools import QUiLoader
from PySide6.QtWidgets import (
    QAbstractItemView,
    QHeaderView,
    QLabel,
    QLineEdit,
    QMainWindow,
    QPushButton,
    QTableWidget,
    QWidget,
)


class MainWindow(QMainWindow):
    """메인 UI 로딩과 위젯 참조 제공."""

    def __init__(self):
        super().__init__()
        self._logger = logging.getLogger(self.__class__.__name__)
        self.ui = self._load_ui("mainwindow.ui")
        if isinstance(self.ui, QWidget):
            self.setCentralWidget(self.ui)
        self._bind_widgets()
        self._apply_style()

    def _load_ui(self, filename):
        """Qt Designer UI 파일을 로딩한다."""
        ui_path = Path(__file__).resolve().parent / filename
        loader = QUiLoader()
        file = QFile(str(ui_path))
        try:
            if not file.open(QFile.ReadOnly):
                self._logger.error("UI open failed: %s", ui_path)
                return QWidget()
            widget = loader.load(file)
            if widget is None:
                self._logger.error("UI load failed: %s", ui_path)
                return QWidget()
            return widget
        finally:
            file.close()

    def _bind_widgets(self):
        """주요 위젯을 속성으로 연결한다."""
        self.searchLineEdit = self.ui.findChild(QLineEdit, "searchLineEdit")
        self.inventoryTable = self.ui.findChild(QTableWidget, "inventoryTable")
        self.inboundButton = self.ui.findChild(QPushButton, "inboundButton")
        self.outboundButton = self.ui.findChild(QPushButton, "outboundButton")
        self.orderButton = self.ui.findChild(QPushButton, "orderButton")
        self.returnButton = self.ui.findChild(QPushButton, "returnButton")
        self.moveButton = self.ui.findChild(QPushButton, "moveButton")
        self.dashboardButton = self.ui.findChild(QPushButton, "dashboardButton")
        self.undoButton = self.ui.findChild(QPushButton, "undoButton")
        self.refreshButton = self.ui.findChild(QPushButton, "refreshButton")
        self.approvalButton = self.ui.findChild(QPushButton, "approvalButton")
        self.workflowButton = self.ui.findChild(QPushButton, "workflowButton")
        self.safetyBadgeLabel = self.ui.findChild(QLabel, "safetyBadgeLabel")
        self.statusLabel = self.ui.findChild(QLabel, "statusLabel")
        self.userInfoLabel = self.ui.findChild(QLabel, "userInfoLabel")

    def _apply_style(self):
        """가독성 중심 기본 스타일과 테이블 동작을 설정한다."""
        self.resize(1320, 760)
        self.setFont(QFont("Apple SD Gothic Neo", 11))
        self.setStyleSheet(
            """
            QWidget { background: #f4f6f8; color: #1c1f23; }
            QLineEdit {
                background: #ffffff;
                border: 1px solid #d0d7de;
                border-radius: 8px;
                padding: 8px;
            }
            QPushButton {
                background: #ffffff;
                border: 1px solid #c9d1d9;
                border-radius: 8px;
                padding: 8px 12px;
                min-height: 34px;
            }
            QPushButton:hover { background: #f0f4f8; }
            QTableWidget {
                background: #ffffff;
                border: 1px solid #d7dde4;
                border-radius: 10px;
                gridline-color: #eef1f4;
                selection-background-color: #d9ecff;
            }
            QHeaderView::section {
                background: #f7f9fb;
                color: #4b5563;
                border: none;
                border-bottom: 1px solid #e5e7eb;
                padding: 8px;
                font-weight: 600;
            }
            """
        )

        if self.searchLineEdit:
            self.searchLineEdit.setPlaceholderText("품목 ID/이름/카테고리/위치 검색")
            self.searchLineEdit.setToolTip("재고 테이블에서 품목과 위치를 빠르게 검색합니다.")

        # 업무 버튼에 간단한 목적 안내를 넣어 초심자도 동선을 이해할 수 있게 한다.
        if self.inboundButton:
            self.inboundButton.setToolTip("구매/납품으로 재고를 증가시킵니다.")
        if self.outboundButton:
            self.outboundButton.setToolTip("판매/사용으로 재고를 감소시킵니다.")
        if self.orderButton:
            self.orderButton.setToolTip("거래처 기준 발주를 생성합니다.")
        if self.returnButton:
            self.returnButton.setToolTip("고객/공급처 반품을 재고에 반영합니다.")
        if self.moveButton:
            self.moveButton.setToolTip("창고/매장 간 재고를 이동합니다.")
        if self.dashboardButton:
            self.dashboardButton.setToolTip("월간 입출고 요약을 조회합니다.")
        if self.approvalButton:
            self.approvalButton.setToolTip("승인 요청 조회/승인/반려를 처리합니다.")
        if self.workflowButton:
            self.workflowButton.setToolTip("병원/쇼핑몰 업종별 특화 업무를 실행합니다.")
        if self.refreshButton:
            self.refreshButton.setToolTip("서버 또는 로컬 데이터로 재고 테이블을 새로고침합니다.")

        if isinstance(self.inventoryTable, QTableWidget):
            table = self.inventoryTable
            table.setAlternatingRowColors(True)
            table.setSelectionBehavior(QAbstractItemView.SelectRows)
            table.setSelectionMode(QAbstractItemView.SingleSelection)
            table.setEditTriggers(QAbstractItemView.NoEditTriggers)
            table.setSortingEnabled(True)
            table.verticalHeader().setVisible(False)
            header = table.horizontalHeader()
            header.setSectionResizeMode(QHeaderView.Stretch)
            header.setSectionResizeMode(0, QHeaderView.ResizeToContents)
            header.setSectionResizeMode(3, QHeaderView.ResizeToContents)
            header.setSectionResizeMode(6, QHeaderView.ResizeToContents)
            table.setFocusPolicy(Qt.NoFocus)
