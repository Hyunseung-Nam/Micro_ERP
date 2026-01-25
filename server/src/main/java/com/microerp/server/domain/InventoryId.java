package com.microerp.server.domain;

import jakarta.persistence.Column;
import jakarta.persistence.Embeddable;
import java.io.Serializable;
import java.util.Objects;

/**
 * 역할: 재고 복합키를 표현한다.
 * 책임: 품목 ID와 위치 ID 조합 보관.
 * 외부 의존성: JPA.
 */
@Embeddable
public class InventoryId implements Serializable {
    @Column(name = "item_id", length = 50)
    private String itemId;

    @Column(name = "location_id", length = 50)
    private String locationId;

    /**
     * 목적: JPA 기본 생성자.
     * Args: 없음
     * Returns: 없음
     * Side Effects: 없음
     * Raises: 없음
     */
    public InventoryId() {
    }

    /**
     * 목적: 복합키를 생성한다.
     * Args:
     *  - itemId: 품목 ID
     *  - locationId: 위치 ID
     * Returns: 없음
     * Side Effects: 없음
     * Raises: 없음
     */
    public InventoryId(String itemId, String locationId) {
        this.itemId = itemId;
        this.locationId = locationId;
    }

    /**
     * 목적: 품목 ID를 반환한다.
     * Args: 없음
     * Returns:
     *  - String: 품목 ID
     * Side Effects: 없음
     * Raises: 없음
     */
    public String getItemId() {
        return itemId;
    }

    /**
     * 목적: 품목 ID를 설정한다.
     * Args:
     *  - itemId: 품목 ID
     * Returns: 없음
     * Side Effects: 없음
     * Raises: 없음
     */
    public void setItemId(String itemId) {
        this.itemId = itemId;
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
     * 목적: 복합키 동등성을 비교한다.
     * Args:
     *  - o: 비교 대상
     * Returns:
     *  - boolean: 동일 여부
     * Side Effects: 없음
     * Raises: 없음
     */
    @Override
    public boolean equals(Object o) {
        if (this == o) {
            return true;
        }
        if (o == null || getClass() != o.getClass()) {
            return false;
        }
        InventoryId that = (InventoryId) o;
        return Objects.equals(itemId, that.itemId)
            && Objects.equals(locationId, that.locationId);
    }

    /**
     * 목적: 복합키 해시를 반환한다.
     * Args: 없음
     * Returns:
     *  - int: 해시값
     * Side Effects: 없음
     * Raises: 없음
     */
    @Override
    public int hashCode() {
        return Objects.hash(itemId, locationId);
    }
}
