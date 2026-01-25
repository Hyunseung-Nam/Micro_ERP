package com.microerp.server.domain;

import jakarta.persistence.Column;
import jakarta.persistence.Entity;
import jakarta.persistence.Id;
import jakarta.persistence.Table;

/**
 * 역할: 재고 위치 정보를 표현한다.
 * 책임: 위치 식별자와 이름 보관.
 * 외부 의존성: JPA.
 */
@Entity
@Table(name = "locations")
public class Location {
    @Id
    @Column(name = "location_id", nullable = false, length = 50)
    private String locationId;

    @Column(name = "name", nullable = false, length = 100)
    private String name;

    /**
     * 목적: JPA 기본 생성자.
     * Args: 없음
     * Returns: 없음
     * Side Effects: 없음
     * Raises: 없음
     */
    public Location() {
    }

    /**
     * 목적: 위치 객체를 생성한다.
     * Args:
     *  - locationId: 위치 ID
     *  - name: 위치명
     * Returns: 없음
     * Side Effects: 없음
     * Raises: 없음
     */
    public Location(String locationId, String name) {
        this.locationId = locationId;
        this.name = name;
    }

    /**
     * 목적: 위치 ID를 반환한다.
     * Args: 없음
     * Returns:
     *  - String: 위치 ID
     * Side Effects: 없음
     * Raises: 없음
     */
    public String getLocationId() {
        return locationId;
    }

    /**
     * 목적: 위치 ID를 설정한다.
     * Args:
     *  - locationId: 위치 ID
     * Returns: 없음
     * Side Effects: 없음
     * Raises: 없음
     */
    public void setLocationId(String locationId) {
        this.locationId = locationId;
    }

    /**
     * 목적: 위치명을 반환한다.
     * Args: 없음
     * Returns:
     *  - String: 위치명
     * Side Effects: 없음
     * Raises: 없음
     */
    public String getName() {
        return name;
    }

    /**
     * 목적: 위치명을 설정한다.
     * Args:
     *  - name: 위치명
     * Returns: 없음
     * Side Effects: 없음
     * Raises: 없음
     */
    public void setName(String name) {
        this.name = name;
    }
}
