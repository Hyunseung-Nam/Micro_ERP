package com.microerp.server.repository;

import com.microerp.server.domain.OrderLine;
import org.springframework.data.jpa.repository.JpaRepository;

/**
 * 역할: 발주 라인 DB 접근을 담당한다.
 * 책임: 발주 라인 조회/저장 JPA 인터페이스 제공.
 * 외부 의존성: Spring Data JPA.
 */
public interface OrderLineRepository extends JpaRepository<OrderLine, Long> {
}
