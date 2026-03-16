# Micro_ERP 백엔드 학습 포인트 정리

이 문서는 `/Users/hyunseung/dev/Micro_ERP/server` 코드를 기준으로,
백엔드 학습에 특히 도움이 되는 부분을 실전 관점에서 정리한 가이드입니다.

## 1) 이 프로젝트로 배우기 좋은 이유

- **실무형 계층 구조**를 갖춤: `Controller -> Service -> Repository -> Domain`
- **인증/인가(JWT + RBAC)** 가 실제 API에 붙어 있음
- **재고/주문/승인/감사로그**처럼 백엔드 핵심 도메인이 연결되어 있음
- **DB 마이그레이션(Flyway)**, **예외 표준화**, **트랜잭션**까지 포함

---

## 2) 핵심 학습 영역과 코드 포인트

### A. API 계층 분리 (Controller / Service / Repository)

학습 포인트:
- Controller는 요청/응답 + 인증 사용자 전달에 집중
- Service는 도메인 규칙/비즈니스 처리 담당
- Repository는 DB 접근만 담당

추천 코드:
- `controller/InventoryController.java`
- `service/InventoryService.java`
- `repository/InventoryRepository.java`

왜 좋은가:
- 역할 분리가 명확해 "어디에 어떤 코드를 써야 하는지" 감각을 익히기 좋음.

---

### B. 인증/인가 설계 (JWT + Spring Security + RBAC)

학습 포인트:
- 로그인 후 JWT 발급, 요청 시 필터에서 인증 컨텍스트 구성
- `@PreAuthorize`로 API별 권한 제어
- 역할(Role) -> 스코프(Scope) 매핑 전략

추천 코드:
- `config/SecurityConfig.java`
- `security/JwtService.java`
- `security/JwtAuthenticationFilter.java`
- `service/RbacService.java`
- `controller/AuthController.java`, `service/AuthService.java`

왜 좋은가:
- 단순 로그인 API를 넘어 실제 권한 모델(역할+세부권한) 운영 방법을 볼 수 있음.

---

### C. 트랜잭션과 도메인 규칙

학습 포인트:
- `@Transactional` 경계 설정
- 재고 음수 방지 같은 무결성 규칙을 Service에서 강제
- 주문 상태 전이(`SUBMITTED -> APPROVED -> CLOSED`) 처리

추천 코드:
- `service/InventoryService.java`
- `service/OrderService.java`
- `service/WorkflowService.java`

왜 좋은가:
- "DB는 되는데 비즈니스는 깨지는" 문제를 예방하는 백엔드 핵심 감각을 익힘.

---

### D. 승인(Approval) 워크플로우

학습 포인트:
- 변경 요청을 즉시 반영하지 않고 승인 요청으로 분리
- 승인 시점에 실제 실행(`executeApproval`)하는 구조
- payload 기반 다형 처리(재고조정/주문종결)

추천 코드:
- `controller/ApprovalController.java`
- `service/ApprovalService.java`
- `domain/ApprovalRequest.java`
- `repository/ApprovalRequestRepository.java`

왜 좋은가:
- 운영 리스크가 큰 작업에 대한 **통제 가능한 백엔드 설계**를 배울 수 있음.

---

### E. 감사 로그(Audit Log)

학습 포인트:
- 인증, 재고조정, 주문상태변경, 승인행위 등을 로그로 남김
- "누가/언제/무엇을" 추적 가능한 형태

추천 코드:
- `service/AuditLogService.java`
- `controller/AuditController.java`
- `domain/AuditLog.java`

왜 좋은가:
- 기능 구현을 넘어, 운영/감사/사후분석까지 고려하는 백엔드 사고를 훈련할 수 있음.

---

### F. DB 스키마와 마이그레이션(Flyway)

학습 포인트:
- DDL을 코드와 분리해 버전 관리
- 초기 스키마 + 기능 확장 스키마를 단계적으로 관리

추천 코드:
- `resources/db/migration/V1__init.sql`
- `resources/db/migration/V2__approval_audit_workflow.sql`
- `resources/application.yml` (`ddl-auto: validate` 설정 포함)

왜 좋은가:
- 팀/운영 환경에서 필수인 "스키마 변경 이력 관리" 습관을 익힘.

---

### G. 예외 처리 표준화

학습 포인트:
- 도메인 예외(`ApiException`)와 공통 핸들러 분리
- Validation/DB/기타 예외 응답 포맷 일관화

추천 코드:
- `exception/ApiException.java`
- `exception/GlobalExceptionHandler.java`
- `exception/ErrorResponse.java`

왜 좋은가:
- 프론트/클라이언트가 소비하기 쉬운 안정적 API 에러 계약을 만들 수 있음.

---

### H. JPA 매핑 심화 (복합키, 연관관계)

학습 포인트:
- `@Embeddable`, `@EmbeddedId`, `@MapsId`를 이용한 복합키 매핑
- 주문-라인(`@OneToMany`), 품목-재고 등 연관관계 관리

추천 코드:
- `domain/InventoryId.java`
- `domain/Inventory.java`
- `domain/Order.java`
- `domain/OrderLine.java`

왜 좋은가:
- 실무에서 자주 어려워하는 JPA 매핑 케이스를 작은 범위에서 학습 가능.

---

## 3) 추천 학습 순서 (실전형)

1. `InventoryController -> InventoryService -> Inventory` 흐름 읽기
2. `AuthService/JwtService/SecurityConfig`로 인증 흐름 이해
3. `RbacService + @PreAuthorize`로 권한 제어 추적
4. `OrderService` 상태 전이 규칙 분석
5. `ApprovalService` 승인 워크플로우 이해
6. `AuditLogService`로 행위 추적 설계 확인
7. `V1/V2` 마이그레이션으로 DB 버전 관리 방식 익히기

---

## 4) 바로 해볼 백엔드 실습 과제

### 과제 1. 재고 조정 사유 코드 표준화
- 목표: `reason` 문자열 자유 입력 대신 코드(enum) 기반으로 관리
- 학습 포인트: DTO 검증 + Service 규칙 + 감사로그 구조화

### 과제 2. 승인 요청 타입 추가
- 목표: `REQUEST_TYPE_*` 새 타입 추가 후 승인 실행 로직 연결
- 학습 포인트: 확장 가능한 워크플로우 설계

### 과제 3. 감사 로그 검색 API
- 목표: 기간/사용자/행위 필터링 조회 추가
- 학습 포인트: 조회 최적화, 인덱스, 페이징

### 과제 4. JWT 만료/재발급 전략
- 목표: Access Token 짧게, Refresh Token 정책 설계
- 학습 포인트: 인증 보안 운영 설계

---

## 5) 학습 시 주의할 점

- `server/README.md`에 "로컬 테스트용"으로 명시되어 있으므로,
  프로덕션 수준 보안/운영 기준(비밀키 관리, 모니터링, 토큰 전략, 감사보관정책)은 별도로 강화해야 합니다.
- 현재 구조는 학습/프로토타입으로 매우 적합하지만,
  대규모 트래픽/멀티노드 환경을 전제로 하지는 않습니다.

---

## 6) 한 줄 요약

이 프로젝트의 백엔드는 "작지만 실무 핵심(인증/권한, 트랜잭션, 승인, 감사, 마이그레이션)"이 모여 있어,
백엔드 입문에서 중급으로 넘어갈 때 매우 좋은 학습 재료입니다.
