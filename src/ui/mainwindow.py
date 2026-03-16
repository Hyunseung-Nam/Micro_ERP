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
        """현대적인 운영 콘솔 톤으로 스타일과 상호작용을 설정한다."""
        self.resize(1320, 760)
        self.setFont(QFont("Apple SD Gothic Neo", 11))
        self.setStyleSheet(
            """
            QWidget { background: #eef3fb; color: #162032; }
            QLineEdit {
                background: #ffffff;
                border: 1px solid #c7d2e5;
                border-radius: 12px;
                padding: 10px 12px;
            }
            QLineEdit:focus { border: 2px solid #2563eb; }
            QPushButton {
                background: #ffffff;
                border: 1px solid #c7d0df;
                border-radius: 12px;
                padding: 8px 12px;
                min-height: 36px;
                font-weight: 600;
            }
            QPushButton:hover { background: #edf3ff; border-color: #94a8cc; }
            QPushButton#inboundButton, QPushButton#orderButton, QPushButton#approvalButton {
                background: #2563eb;
                border: 1px solid #1d4ed8;
                color: #ffffff;
            }
            QPushButton#inboundButton:hover, QPushButton#orderButton:hover, QPushButton#approvalButton:hover {
                background: #1e40af;
            }
            QPushButton#outboundButton, QPushButton#returnButton {
                background: #fff4f1;
                border: 1px solid #fecaca;
                color: #9a3412;
            }
            QPushButton#outboundButton:hover, QPushButton#returnButton:hover {
                background: #ffe7df;
            }
            QTableWidget {
                background: #ffffff;
                border: 1px solid #cfd8e7;
                border-radius: 14px;
                gridline-color: #edf2f8;
                selection-background-color: #d9e7ff;
            }
            QHeaderView::section {
                background: #f4f7fd;
                color: #3b4e68;
                border: none;
                border-bottom: 1px solid #dde5f2;
                padding: 9px;
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
