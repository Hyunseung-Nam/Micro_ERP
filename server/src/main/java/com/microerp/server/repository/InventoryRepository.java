package com.microerp.server.repository;

import com.microerp.server.domain.Inventory;
import com.microerp.server.domain.InventoryId;
import org.springframework.data.jpa.repository.JpaRepository;

/**
 * 역할: 재고 DB 접근을 담당한다.
 * 책임: 재고 조회/저장 JPA 인터페이스 제공.
 * 외부 의존성: Spring Data JPA.
 */
public interface InventoryRepository extends JpaRepository<Inventory, InventoryId> {
}
