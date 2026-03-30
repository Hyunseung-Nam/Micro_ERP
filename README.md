# Micro ERP System

도매/소매/쇼핑몰/병원 시나리오를 지원하는 로컬 ERP 개발 프로젝트입니다.

## 오늘 반영된 주요 내용
- Python 데스크톱 앱 UI/UX 개선 (가독성, 검색, 상태 표시, 안전재고 강조)
- Spring API 연동 모드 추가 (`ERP_USE_API=true`)
- 업종 워크플로우 추가
  - 병원 사용량 차감
  - 쇼핑몰 반품/교환
- 권한 체계(RBAC) + 승인 플로우 + 감사 로그 추가
- 웹 대시보드 `dashboard.html`을 운영 콘솔형 화면으로 개편

## 프레임워크/스택
- Desktop: Python 3, PySide6
- Backend API: Java 25, Spring Boot 3.3.2, Spring Security(JWT), Spring Data JPA, Flyway
- DB: MySQL 8+ (로컬 테스트는 MySQL 9.6으로도 동작 확인)

## 프로젝트 구성
- `src/`: PySide6 기반 데스크톱 앱
- `server/`: Spring Boot API 서버
- `server/src/main/resources/static/dashboard.html`: 웹 운영 콘솔

## 실행 방법
### 1) MySQL 시작
```bash
brew services start mysql
```

### 2) Spring 서버 실행
```bash
cd /Users/hyunseung/dev/Micro_ERP/server
export PATH="/opt/homebrew/opt/openjdk/bin:$PATH"
mvn -DskipTests -Dmaven.repo.local=/Users/hyunseung/dev/Micro_ERP/.m2 spring-boot:run
```

### 3) 웹 운영 콘솔 접속
- `http://localhost:8080/dashboard.html`

### 4) 데스크톱 앱 실행(API 연동 모드)
```bash
cd /Users/hyunseung/dev/Micro_ERP
export ERP_PROFILE=hospital  # wholesale / retail / ecommerce / hospital / general
export ERP_USE_API=true
export ERP_API_BASE_URL=http://localhost:8080
python3 src/main.py
```

## 기본 계정
- `admin / admin123`
- `manager / manager123`
- `staff / staff123`
- `auditor / auditor123`

## 핵심 기능
- 재고 조회/조정, 발주 생성/승인/종결
- 승인 요청 생성/승인/반려
- 감사 로그 조회
- 업종 워크플로우 API
  - `POST /api/workflows/hospital/consume`
  - `POST /api/workflows/ecommerce/return-exchange`

## 환경 변수
- `ERP_USE_API` (기본: `true`)
- `ERP_API_BASE_URL` (기본: `http://localhost:8080`)
- `ERP_PROFILE` (`wholesale`, `retail`, `ecommerce`, `hospital`, `general`)
- `ERP_DB_USER`, `ERP_DB_PASSWORD`, `ERP_JWT_SECRET`

## 참고
- 로컬 테스트 전용입니다.

---

## 리팩터링 이력

### 2025-03-19: 확장성·유지보수성 개선 (refactoring.mdc 준수)

**목표**  
입력/출력·UX·데이터·API·config·파일 구조는 유지한 채, Controller 비대화 해소 및 책임 분리.

**변경 요약**
- **재고 테이블 행 로직 분리**: `modules/inventory_table_builder.py` 추가
  - `build_inventory_rows(inventory, items, search_text, shortage_ids)`로 테이블용 행 리스트 생성
  - `INVENTORY_TABLE_HEADERS` 상수로 헤더 정의
  - UI 없이 단위 테스트·재사용 가능
- **다이얼로그 공통 로직 분리**: `ui/dialog_helpers.py` 추가
  - `DialogHelper`: UI 로딩, 스타일, 프리필, 폼 수집, 액션/폼 다이얼로그
  - Controller는 `DialogHelper`에 위임하여 다이얼로그 처리
- **Controller 역할 축소**: 이벤트 연결 → 서비스/API 호출 → 화면 갱신만 담당 (오케스트레이션)

**영향 파일**
- `src/modules/controller.py` (리팩터, 내부 private 메서드 제거)
- `src/modules/inventory_table_builder.py` (신규)
- `src/ui/dialog_helpers.py` (신규)
- `tests/verify_refactor.py` (신규, 검증 스크립트)

**검증**
- `python3 tests/verify_refactor.py`: 재고 행 빌더·모듈 참조 동작 확인
- 기존 `tests/test_inventory_rules.py` 통과

**리스크**
- 낮음. 공개 API·config·DB·실행 방식 변경 없음.

**롤백**
- `inventory_table_builder.py`, `ui/dialog_helpers.py` 삭제 후, controller.py를 이전 버전으로 복원.
