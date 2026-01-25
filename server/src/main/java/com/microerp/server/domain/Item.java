package com.microerp.server.domain;

import jakarta.persistence.Column;
import jakarta.persistence.Entity;
import jakarta.persistence.Id;
import jakarta.persistence.Table;

/**
 * 역할: 품목 정보를 표현한다.
 * 책임: 품목명, 단위, 안전재고 보관.
 * 외부 의존성: JPA.
 */
@Entity
@Table(name = "items")
public class Item {
    @Id
    @Column(name = "item_id", nullable = false, length = 50)
    private String itemId;

    @Column(name = "name", nullable = false, length = 100)
    private String name;

    @Column(name = "unit", nullable = false, length = 20)
    private String unit;

    @Column(name = "safety_stock", nullable = false)
    private int safetyStock;

    /**
     * 목적: JPA 기본 생성자.
     * Args: 없음
     * Returns: 없음
     * Side Effects: 없음
     * Raises: 없음
     */
    public Item() {
    }

    /**
     * 목적: 품목 객체를 생성한다.
     * Args:
     *  - itemId: 품목 ID
     *  - name: 품목명
     *  - unit: 단위
     *  - safetyStock: 안전재고
     * Returns: 없음
     * Side Effects: 없음
     * Raises: 없음
     */
    public Item(String itemId, String name, String unit, int safetyStock) {
        this.itemId = itemId;
        this.name = name;
        this.unit = unit;
        this.safetyStock = safetyStock;
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
     * 목적: 품목명을 반환한다.
     * Args: 없음
     * Returns:
     *  - String: 품목명
     * Side Effects: 없음
     * Raises: 없음
     */
    public String getName() {
        return name;
    }

    /**
     * 목적: 품목명을 설정한다.
     * Args:
     *  - name: 품목명
     * Returns: 없음
     * Side Effects: 없음
     * Raises: 없음
     */
    public void setName(String name) {
        this.name = name;
    }

    /**
     * 목적: 단위를 반환한다.
     * Args: 없음
     * Returns:
     *  - String: 단위
     * Side Effects: 없음
     * Raises: 없음
     */
    public String getUnit() {
        return unit;
    }

    /**
     * 목적: 단위를 설정한다.
     * Args:
     *  - unit: 단위
     * Returns: 없음
     * Side Effects: 없음
     * Raises: 없음
     */
    public void setUnit(String unit) {
        this.unit = unit;
    }

    /**
     * 목적: 안전재고를 반환한다.
     * Args: 없음
     * Returns:
     *  - int: 안전재고
     * Side Effects: 없음
     * Raises: 없음
     */
    public int getSafetyStock() {
        return safetyStock;
    }

    /**
     * 목적: 안전재고를 설정한다.
     * Args:
     *  - safetyStock: 안전재고
     * Returns: 없음
     * Side Effects: 없음
     * Raises: 없음
     */
    public void setSafetyStock(int safetyStock) {
        this.safetyStock = safetyStock;
    }
}
