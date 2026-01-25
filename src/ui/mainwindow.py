import logging
from pathlib import Path

from PySide6.QtCore import QFile
from PySide6.QtUiTools import QUiLoader
from PySide6.QtWidgets import (
    QLineEdit,
    QMainWindow,
    QPushButton,
    QLabel,
    QTableWidget,
    QWidget,
)


class MainWindow(QMainWindow):
    """
    역할: 메인 UI 로딩과 위젯 참조 제공
    책임: UI 파일 로딩, 위젯 바인딩, 메인 화면 표시
    외부 의존성: PySide6, `src/ui/mainwindow.ui`
    """

    def __init__(self):
        super().__init__()
        self._logger = logging.getLogger(self.__class__.__name__)
        self.ui = self._load_ui("mainwindow.ui")
        if isinstance(self.ui, QWidget):
            self.setCentralWidget(self.ui)
        self._bind_widgets()

    def _load_ui(self, filename):
        """
        목적: Qt Designer UI 파일을 로딩한다.
        Args:
            filename (str): UI 파일명
        Returns:
            QWidget: 로딩된 UI 위젯
        Side Effects:
            UI 파일 접근
        Raises:
            없음
        """
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
        """
        목적: 주요 위젯을 속성으로 연결한다.
        Args:
            없음
        Returns:
            None
        Side Effects:
            위젯 속성 설정
        Raises:
            없음
        """
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
        self.safetyBadgeLabel = self.ui.findChild(QLabel, "safetyBadgeLabel")
        self.statusLabel = self.ui.findChild(QLabel, "statusLabel")
