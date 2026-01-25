package com.microerp.server.repository;

import com.microerp.server.domain.Partner;
import org.springframework.data.jpa.repository.JpaRepository;

/**
 * 역할: 거래처 DB 접근을 담당한다.
 * 책임: 거래처 조회/저장 JPA 인터페이스 제공.
 * 외부 의존성: Spring Data JPA.
 */
public interface PartnerRepository extends JpaRepository<Partner, String> {
}
