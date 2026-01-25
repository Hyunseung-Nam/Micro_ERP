import logging
from datetime import datetime
from pathlib import Path
from shutil import copy2

from config import get_data_dir

_LOGGER = logging.getLogger(__name__)


def create_backup(data_dir=None):
    """
    목적: 데이터 디렉터리를 타임스탬프 기반으로 백업한다.
    Args:
        data_dir (Path|None): 데이터 디렉터리 경로
    Returns:
        bool: 성공 여부
    Side Effects:
        백업 디렉터리 생성 및 파일 복사
    Raises:
        없음
    """
    target_dir = Path(data_dir) if data_dir else get_data_dir()
    backup_root = target_dir / "backup"
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_dir = backup_root / timestamp
    try:
        backup_dir.mkdir(parents=True, exist_ok=True)
        for file_path in target_dir.glob("*.json"):
            copy2(file_path, backup_dir / file_path.name)
        return True
    except OSError as exc:
        _LOGGER.error("Backup failed: %s", exc)
        return False
