import logging
from pathlib import Path

from PySide6.QtWidgets import QApplication

from config import APP_NAME, get_log_dir
from modules import storage
from modules.controller import MainController
from ui.mainwindow import MainWindow


def _setup_logging():
    """
    목적: 로깅 설정을 초기화한다.
    Args:
        없음
    Returns:
        None
    Side Effects:
        로그 디렉터리 생성 및 로깅 핸들러 설정
    Raises:
        없음
    """
    log_dir = get_log_dir()
    try:
        log_dir.mkdir(parents=True, exist_ok=True)
    except OSError:
        log_dir = Path(".")
    log_path = log_dir / "app.log"
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(name)s - %(message)s",
        handlers=[
            logging.FileHandler(log_path, encoding="utf-8"),
            logging.StreamHandler(),
        ],
    )


def main():
    """
    목적: 애플리케이션을 실행한다.
    Args:
        없음
    Returns:
        int: 종료 코드
    Side Effects:
        Qt 애플리케이션 실행
    Raises:
        없음
    """
    _setup_logging()
    storage.ensure_data_files()
    app = QApplication([])
    window = MainWindow()
    controller = MainController(window)
    controller.refresh_inventory_table()
    window.setWindowTitle(APP_NAME)
    window.show()
    return app.exec()


if __name__ == "__main__":
    raise SystemExit(main())
