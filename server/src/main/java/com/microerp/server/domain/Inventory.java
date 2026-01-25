package com.microerp.server.domain;

import jakarta.persistence.Column;
import jakarta.persistence.EmbeddedId;
import jakarta.persistence.Entity;
import jakarta.persistence.FetchType;
import jakarta.persistence.JoinColumn;
import jakarta.persistence.ManyToOne;
import jakarta.persistence.MapsId;
import jakarta.persistence.Table;

/**
 * 역할: 품목별 위치 재고를 표현한다.
 * 책임: 수량 및 품목/위치 연계 보관.
 * 외부 의존성: JPA.
 */
@Entity
@Table(name = "inventory")
public class Inventory {
    @EmbeddedId
    private InventoryId id;

    @MapsId("itemId")
    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "item_id")
    private Item item;

    @MapsId("locationId")
    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "location_id")
    private Location location;

    @Column(name = "quantity", nullable = false)
    private int quantity;

    /**
     * 목적: JPA 기본 생성자.
     * Args: 없음
     * Returns: 없음
     * Side Effects: 없음
     * Raises: 없음
     */
    public Inventory() {
    }

    /**
     * 목적: 재고 객체를 생성한다.
     * Args:
     *  - item: 품목
     *  - location: 위치
     *  - quantity: 수량
     * Returns: 없음
     * Side Effects: 없음
     * Raises: 없음
     */
    public Inventory(Item item, Location location, int quantity) {
        this.id = new InventoryId(item.getItemId(), location.getLocationId());
        this.item = item;
        this.location = location;
        this.quantity = quantity;
    }

    /**
     * 목적: 복합키를 반환한다.
     * Args: 없음
     * Returns:
     *  - InventoryId: 복합키
     * Side Effects: 없음
     * Raises: 없음
     */
    public InventoryId getId() {
        return id;
    }

    /**
     * 목적: 복합키를 설정한다.
     * Args:
     *  - id: 복합키
     * Returns: 없음
     * Side Effects: 없음
     * Raises: 없음
     */
    public void setId(InventoryId id) {
        this.id = id;
    }

    /**
     * 목적: 품목 정보를 반환한다.
     * Args: 없음
     * Returns:
     *  - Item: 품목
     * Side Effects: 없음
     * Raises: 없음
     */
    public Item getItem() {
        return item;
    }

    /**
     * 목적: 품목 정보를 설정한다.
     * Args:
     *  - item: 품목
     * Returns: 없음
     * Side Effects: 없음
     * Raises: 없음
     */
    public void setItem(Item item) {
        this.item = item;
    }

    /**
     * 목적: 위치 정보를 반환한다.
     * Args: 없음
     * Returns:
     *  - Location: 위치
     * Side Effects: 없음
     * Raises: 없음
     */
    public Location getLocation() {
        return location;
    }

    /**
     * 목적: 위치 정보를 설정한다.
     * Args:
     *  - location: 위치
     * Returns: 없음
     * Side Effects: 없음
     * Raises: 없음
     */
    public void setLocation(Location location) {
        this.location = location;
    }

    /**
     * 목적: 수량을 반환한다.
     * Args: 없음
     * Returns:
     *  - int: 수량
     * Side Effects: 없음
     * Raises: 없음
     */
    public int getQuantity() {
        return quantity;
    }

    /**
     * 목적: 수량을 설정한다.
     * Args:
     *  - quantity: 수량
     * Returns: 없음
     * Side Effects: 없음
     * Raises: 없음
     */
    public void setQuantity(int quantity) {
        this.quantity = quantity;
    }
}
