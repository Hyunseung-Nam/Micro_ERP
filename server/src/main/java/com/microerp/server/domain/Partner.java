package com.microerp.server.domain;

import jakarta.persistence.Column;
import jakarta.persistence.Entity;
import jakarta.persistence.Id;
import jakarta.persistence.Table;

/**
 * 역할: 거래처 정보를 표현한다.
 * 책임: 거래처 식별자, 유형, 이름 보관.
 * 외부 의존성: JPA.
 */
@Entity
@Table(name = "partners")
public class Partner {
    @Id
    @Column(name = "partner_id", nullable = false, length = 50)
    private String partnerId;

    @Column(name = "name", nullable = false, length = 100)
    private String name;

    @Column(name = "type", nullable = false, length = 20)
    private String type;

    /**
     * 목적: JPA 기본 생성자.
     * Args: 없음
     * Returns: 없음
     * Side Effects: 없음
     * Raises: 없음
     */
    public Partner() {
    }

    /**
     * 목적: 거래처 객체를 생성한다.
     * Args:
     *  - partnerId: 거래처 ID
     *  - name: 거래처명
     *  - type: 거래처 유형
     * Returns: 없음
     * Side Effects: 없음
     * Raises: 없음
     */
    public Partner(String partnerId, String name, String type) {
        this.partnerId = partnerId;
        this.name = name;
        this.type = type;
    }

    /**
     * 목적: 거래처 ID를 반환한다.
     * Args: 없음
     * Returns:
     *  - String: 거래처 ID
     * Side Effects: 없음
     * Raises: 없음
     */
    public String getPartnerId() {
        return partnerId;
    }

    /**
     * 목적: 거래처 ID를 설정한다.
     * Args:
     *  - partnerId: 거래처 ID
     * Returns: 없음
     * Side Effects: 없음
     * Raises: 없음
     */
    public void setPartnerId(String partnerId) {
        this.partnerId = partnerId;
    }

    /**
     * 목적: 거래처명을 반환한다.
     * Args: 없음
     * Returns:
     *  - String: 거래처명
     * Side Effects: 없음
     * Raises: 없음
     */
    public String getName() {
        return name;
    }

    /**
     * 목적: 거래처명을 설정한다.
     * Args:
     *  - name: 거래처명
     * Returns: 없음
     * Side Effects: 없음
     * Raises: 없음
     */
    public void setName(String name) {
        this.name = name;
    }

    /**
     * 목적: 거래처 유형을 반환한다.
     * Args: 없음
     * Returns:
     *  - String: 거래처 유형
     * Side Effects: 없음
     * Raises: 없음
     */
    public String getType() {
        return type;
    }

    /**
     * 목적: 거래처 유형을 설정한다.
     * Args:
     *  - type: 거래처 유형
     * Returns: 없음
     * Side Effects: 없음
     * Raises: 없음
     */
    public void setType(String type) {
        this.type = type;
    }
}
