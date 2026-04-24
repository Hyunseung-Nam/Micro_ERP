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
        
        # Sidebar Buttons - 명시적 바인딩 및 디버그 확인
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
        
        # Summary Cards
        self.card1Value = self.ui.findChild(QLabel, "card1Value")
        self.card2Value = self.ui.findChild(QLabel, "card2Value")
        self.card3Value = self.ui.findChild(QLabel, "card3Value")
        
        # 바인딩 상태 로그 (개발 모드)
        missing = [name for name, btn in {
            "inbound": self.inboundButton, "outbound": self.outboundButton,
            "order": self.orderButton, "return": self.returnButton, "move": self.moveButton
        }.items() if not btn]
        if missing:
            self._logger.error(f"Critical Sidebar Buttons Missing: {missing}")

    def _apply_style(self):
        """현대적인 운영 콘솔 톤으로 스타일과 상호작용을 설정한다."""
        self.resize(1400, 900)
        self.setFont(QFont("Apple SD Gothic Neo", 10))
        
        # 버튼 스타일을 더 범용적이고 확실하게 수정
        self.setStyleSheet(
            """
            QMainWindow, QWidget#MainWindowWidget { background: #f8fafc; color: #1e293b; }
            
            /* Sidebar Styling */
            QFrame#sidebarFrame {
                background: #1e293b;
                border: none;
                min-width: 240px;
            }
            QLabel#appLogoLabel {
                color: #f1f5f9;
                font-size: 20px;
                font-weight: 800;
                margin-bottom: 20px;
                padding: 10px;
            }
            QLabel#inventoryGroupLabel, QLabel#orderGroupLabel, QLabel#systemGroupLabel {
                color: #64748b;
                font-size: 11px;
                font-weight: 700;
                text-transform: uppercase;
                margin-top: 15px;
                padding-left: 8px;
            }
            
            /* 사이드바 내 모든 버튼에 대한 더 강력한 스타일 정의 */
            #sidebarFrame QPushButton {
                background-color: #243147;
                border: 1px solid #1e293b;
                border-radius: 8px;
                color: #cbd5e1;
                padding: 12px 16px;
                text-align: left;
                font-weight: 600;
                font-size: 13px;
                margin: 2px 0px;
            }
            #sidebarFrame QPushButton:hover {
                background-color: #334155;
                color: #f8fafc;
                border-color: #475569;
            }
            #sidebarFrame QPushButton:pressed {
                background-color: #0f172a;
            }
            
            /* Content Area Styling */
            QFrame#contentFrame {
                background: #f8fafc;
                border: none;
            }
            QLineEdit {
                background: #ffffff;
                border: 1px solid #e2e8f0;
                border-radius: 10px;
                padding: 10px 15px;
                color: #1e293b;
                font-size: 14px;
            }
            QLineEdit:focus {
                border: 2px solid #2563eb;
            }
            
            QLabel#safetyBadgeLabel {
                background: #eff6ff;
                color: #1e40af;
                padding: 8px 16px;
                border-radius: 18px;
                font-weight: 700;
                font-size: 12px;
            }
            
            QPushButton#refreshButton {
                background: #1e3a8a;
                border: none;
                color: #ffffff;
                padding: 10px 20px;
                border-radius: 10px;
                font-weight: 700;
                text-align: center;
            }
            QPushButton#refreshButton:hover {
                background: #1e40af;
            }
            
            QTableWidget {
                background: #ffffff;
                border: 1px solid #e2e8f0;
                border-radius: 15px;
                gridline-color: #f1f5f9;
                selection-background-color: #3b82f6;
                selection-color: #ffffff;
                outline: none;
                color: #1e293b;
                padding: 5px;
            }
            QHeaderView::section {
                background: #f8fafc;
                color: #475569;
                padding: 15px;
                border: none;
                border-bottom: 2px solid #3b82f6;
                font-weight: 800;
                font-size: 12px;
                text-transform: uppercase;
            }
            QTableWidget::item {
                padding: 10px;
                border-bottom: 1px solid #f1f5f9;
            }
            
            /* Global MessageBox Fix */
            QMessageBox {
                background-color: #ffffff;
            }
            QMessageBox QLabel {
                color: #1e293b;
                font-size: 14px;
                min-width: 400px;
            }
            QMessageBox QPushButton {
                background: #f8fafc;
                border: 1px solid #e2e8f0;
                border-radius: 8px;
                padding: 8px 16px;
                min-width: 80px;
                font-weight: 700;
                color: #1e293b;
            }
            QMessageBox QPushButton:hover {
                background: #f1f5f9;
                color: #1e293b;
            }
            
            QLabel#statusLabel {
                color: #64748b;
                font-size: 12px;
                font-weight: 500;
            }
            
            QLabel#userInfoLabel {
                color: #cbd5e1;
                font-size: 13px;
                background: #334155;
                padding: 15px;
                border-radius: 10px;
                margin-top: 15px;
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
            table.verticalHeader().setDefaultSectionSize(48)  # 더 여유로운 행 높이
            header = table.horizontalHeader()
            header.setSectionResizeMode(QHeaderView.Stretch)
            header.setSectionResizeMode(0, QHeaderView.ResizeToContents)
            header.setSectionResizeMode(3, QHeaderView.ResizeToContents)
            header.setSectionResizeMode(6, QHeaderView.ResizeToContents)
            header.setMinimumHeight(50)  # 더 여유로운 헤더 높이
            table.setFocusPolicy(Qt.NoFocus)
            table.setShowGrid(False)  # 현대적인 무격자 스타일
