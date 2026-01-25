import os
from pathlib import Path

APP_NAME = "Micro ERP System"
DATA_DIR_NAME = "data"
LOG_DIR_NAME = "logs"


def get_base_dir():
    """
    목적: 프로젝트 루트 경로를 반환한다.
    Args:
        없음
    Returns:
        Path: 프로젝트 루트 경로
    Side Effects:
        없음
    Raises:
        없음
    """
    return Path(__file__).resolve().parents[1]


def get_data_dir():
    """
    목적: 데이터 디렉터리 경로를 반환한다.
    Args:
        없음
    Returns:
        Path: 데이터 디렉터리 경로
    Side Effects:
        없음
    Raises:
        없음
    """
    return get_base_dir() / DATA_DIR_NAME


def get_log_dir():
    """
    목적: 로그 디렉터리 경로를 반환한다.
    Args:
        없음
    Returns:
        Path: 로그 디렉터리 경로
    Side Effects:
        없음
    Raises:
        없음
    """
    return get_base_dir() / LOG_DIR_NAME


def get_default_user():
    """
    목적: 기본 사용자 식별자를 반환한다.
    Args:
        없음
    Returns:
        str: 기본 사용자 식별자
    Side Effects:
        없음
    Raises:
        없음
    """
    return os.getenv("ERP_DEFAULT_USER", "local_user")


def is_admin_mode():
    """
    목적: 관리자 모드 여부를 반환한다.
    Args:
        없음
    Returns:
        bool: 관리자 모드 여부
    Side Effects:
        없음
    Raises:
        없음
    """
    value = os.getenv("ERP_ADMIN_MODE", "true").strip().lower()
    return value in {"1", "true", "yes", "y"}
