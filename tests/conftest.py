"""pytest 공통 픽스처 및 경로 설정."""
import sys
from pathlib import Path

# src 디렉터리를 sys.path에 추가
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
