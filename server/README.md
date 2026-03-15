# Micro ERP Server (Local Only)

로컬 테스트용 Java + Spring Boot API 서버입니다. 기존 PySide6 앱/JSON 저장소는 변경하지 않습니다.
현재 작업은 프로토타입 단계입니다.

## 요구 사항
- Java 25+ (런타임)
- Maven 3.8+
- MySQL 8.x (로컬)

## 로컬 MySQL 준비
```sql
CREATE DATABASE micro_erp CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;
```

## 환경 변수 (선택)
- `ERP_DB_USER` (기본값: `root`)
- `ERP_DB_PASSWORD` (기본값: `root`)
- `ERP_JWT_SECRET` (기본값: `change_this_secret_change_this_secret`)
- `ERP_SEED_ADMIN_USERNAME` (기본값: `admin`)
- `ERP_SEED_ADMIN_PASSWORD` (기본값: `admin123`)

## 실행
```bash
cd /Users/hyunseung/dev/Micro_ERP/server
export PATH="/opt/homebrew/opt/openjdk/bin:$PATH"
mvn spring-boot:run
```

## 참고
- Spring Boot 3.3.2는 Java 25 bytecode를 직접 실행할 때 제한이 있어, 컴파일 타겟을 21로 두었습니다.

## 웹 대시보드
- 브라우저에서 `http://localhost:8080/dashboard.html` 접속
- 로그인 후 운영 콘솔(재고 리스크/KPI/승인함/감사로그) 조회

## 기본 계정
- 사용자명: `admin`
- 비밀번호: `admin123`
- 사용자명: `manager` / 비밀번호: `manager123`
- 사용자명: `staff` / 비밀번호: `staff123`
- 사용자명: `auditor` / 비밀번호: `auditor123`

## RBAC / 승인 / 감사
- 역할: `ADMIN`, `MANAGER`, `STAFF`, `AUDITOR`
- 승인 API: `/api/approvals`
- 감사 로그 API: `/api/audit/logs`
- 업종 워크플로우 API:
  - 병원 사용량 차감: `POST /api/workflows/hospital/consume`
  - 쇼핑몰 반품/교환: `POST /api/workflows/ecommerce/return-exchange`

## API 테스트 (curl)
```bash
# 로그인
curl -X POST http://localhost:8080/api/auth/login ^
  -H "Content-Type: application/json" ^
  -d "{\"username\":\"admin\",\"password\":\"admin123\"}"
```

응답에서 `token` 값을 복사해 아래에 사용합니다.

```bash
# 현재 사용자
curl http://localhost:8080/api/auth/me ^
  -H "Authorization: Bearer YOUR_TOKEN"
```

```bash
# 사용자 목록
curl http://localhost:8080/api/users ^
  -H "Authorization: Bearer YOUR_TOKEN"
```

```bash
# 재고 목록
curl http://localhost:8080/api/inventory ^
  -H "Authorization: Bearer YOUR_TOKEN"
```

```bash
# 재고 조정 (예: +5)
curl -X POST http://localhost:8080/api/inventory/adjust ^
  -H "Content-Type: application/json" ^
  -H "Authorization: Bearer YOUR_TOKEN" ^
  -d "{\"itemId\":\"ITEM-001\",\"locationId\":\"LOC-001\",\"deltaQuantity\":5}"
```

```bash
# 발주 생성
curl -X POST http://localhost:8080/api/orders ^
  -H "Content-Type: application/json" ^
  -H "Authorization: Bearer YOUR_TOKEN" ^
  -d "{\"partnerId\":\"PARTNER-001\",\"lines\":[{\"itemId\":\"ITEM-001\",\"quantity\":10,\"unit\":\"EA\"}]}"
```

```bash
# 발주 종결
curl -X POST http://localhost:8080/api/orders/1/close ^
  -H "Authorization: Bearer YOUR_TOKEN"
```

```bash
# 승인 요청 생성 (재고 조정)
curl -X POST http://localhost:8080/api/approvals ^
  -H "Content-Type: application/json" ^
  -H "Authorization: Bearer YOUR_TOKEN" ^
  -d "{\"requestType\":\"INVENTORY_ADJUST\",\"requestPayload\":\"{\\\"itemId\\\":\\\"ITEM-001\\\",\\\"locationId\\\":\\\"LOC-001\\\",\\\"deltaQuantity\\\":-20,\\\"reason\\\":\\\"manual\\\"}\"}"
```

## 주의
- 본 모듈은 로컬 테스트 전용입니다.
- 프로덕션 배포/서명/런처 구조에는 영향을 주지 않습니다.
