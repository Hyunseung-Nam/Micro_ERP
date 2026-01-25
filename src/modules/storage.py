import json
import logging
from contextlib import contextmanager
from pathlib import Path
from tempfile import NamedTemporaryFile

from config import get_data_dir
from modules import backup

_LOGGER = logging.getLogger(__name__)

DATA_FILES = {
    "events.json": [],
    "event_lines.json": [],
    "items.json": [],
    "locations.json": [],
    "partners.json": [],
}


@contextmanager
def _file_lock(lock_path):
    """
    목적: 간단한 파일 락을 제공한다.
    Args:
        lock_path (Path): 락 파일 경로
    Returns:
        Iterator[None]: 컨텍스트 매니저
    Side Effects:
        락 파일 생성/삭제
    Raises:
        OSError: 락 파일 생성 실패
    """
    try:
        if lock_path.exists():
            raise OSError("Lock file exists")
        lock_path.write_text("locked", encoding="utf-8")
        yield
    finally:
        try:
            if lock_path.exists():
                lock_path.unlink()
        except OSError:
            _LOGGER.warning("Failed to remove lock file: %s", lock_path)


def ensure_data_files():
    """
    목적: 데이터 디렉터리와 초기 JSON 파일을 보장한다.
    Args:
        없음
    Returns:
        None
    Side Effects:
        데이터 디렉터리 및 파일 생성
    Raises:
        없음
    """
    data_dir = get_data_dir()
    try:
        data_dir.mkdir(parents=True, exist_ok=True)
    except OSError as exc:
        _LOGGER.error("Failed to create data dir: %s", exc)
        return
    for filename, default in DATA_FILES.items():
        path = data_dir / filename
        if not path.exists():
            save_json(path, default)


def load_json(path, default):
    """
    목적: JSON 파일을 로딩한다.
    Args:
        path (Path): JSON 파일 경로
        default (Any): 기본값
    Returns:
        Any: 로딩된 데이터 또는 기본값
    Side Effects:
        파일 읽기
    Raises:
        없음
    """
    try:
        if not Path(path).exists():
            return default
        with Path(path).open("r", encoding="utf-8") as handle:
            return json.load(handle)
    except (OSError, json.JSONDecodeError) as exc:
        _LOGGER.error("Failed to load json: %s", exc)
        return default


def save_json(path, data):
    """
    목적: JSON 파일을 원자적으로 저장한다.
    Args:
        path (Path): JSON 파일 경로
        data (Any): 저장할 데이터
    Returns:
        bool: 성공 여부
    Side Effects:
        파일 쓰기
    Raises:
        없음
    """
    path = Path(path)
    lock_path = path.with_suffix(path.suffix + ".lock")
    try:
        with _file_lock(lock_path):
            with NamedTemporaryFile("w", delete=False, encoding="utf-8") as temp:
                json.dump(data, temp, ensure_ascii=True, indent=2)
                temp_path = Path(temp.name)
            temp_path.replace(path)
        backup.create_backup(get_data_dir())
        return True
    except OSError as exc:
        _LOGGER.error("Failed to save json: %s", exc)
        return False


def append_json_list(path, item):
    """
    목적: 리스트 JSON 파일에 항목을 추가한다.
    Args:
        path (Path): JSON 파일 경로
        item (Any): 추가할 항목
    Returns:
        bool: 성공 여부
    Side Effects:
        파일 읽기/쓰기
    Raises:
        없음
    """
    data = load_json(path, [])
    if not isinstance(data, list):
        data = []
    data.append(item)
    return save_json(path, data)


def load_all_data():
    """
    목적: 모든 데이터 파일을 로딩한다.
    Args:
        없음
    Returns:
        dict: 데이터 딕셔너리
    Side Effects:
        파일 읽기
    Raises:
        없음
    """
    data_dir = get_data_dir()
    return {
        "events": load_json(data_dir / "events.json", []),
        "event_lines": load_json(data_dir / "event_lines.json", []),
        "items": load_json(data_dir / "items.json", []),
        "locations": load_json(data_dir / "locations.json", []),
        "partners": load_json(data_dir / "partners.json", []),
    }
