package com.microerp.server.domain;

import jakarta.persistence.Column;
import jakarta.persistence.Entity;
import jakarta.persistence.FetchType;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.GenerationType;
import jakarta.persistence.Id;
import jakarta.persistence.JoinColumn;
import jakarta.persistence.ManyToOne;
import jakarta.persistence.Table;

/**
 * 역할: 발주 라인 정보를 표현한다.
 * 책임: 품목, 수량, 단위 보관.
 * 외부 의존성: JPA.
 */
@Entity
@Table(name = "order_lines")
public class OrderLine {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    @Column(name = "line_id")
    private Long id;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "order_id")
    private Order order;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "item_id")
    private Item item;

    @Column(name = "quantity", nullable = false)
    private int quantity;

    @Column(name = "unit", nullable = false, length = 20)
    private String unit;

    /**
     * 목적: JPA 기본 생성자.
     * Args: 없음
     * Returns: 없음
     * Side Effects: 없음
     * Raises: 없음
     */
    public OrderLine() {
    }

    /**
     * 목적: 발주 라인을 생성한다.
     * Args:
     *  - item: 품목
     *  - quantity: 수량
     *  - unit: 단위
     * Returns: 없음
     * Side Effects: 없음
     * Raises: 없음
     */
    public OrderLine(Item item, int quantity, String unit) {
        this.item = item;
        this.quantity = quantity;
        this.unit = unit;
    }

    /**
     * 목적: 라인 ID를 반환한다.
     * Args: 없음
     * Returns:
     *  - Long: 라인 ID
     * Side Effects: 없음
     * Raises: 없음
     */
    public Long getId() {
        return id;
    }

    /**
     * 목적: 라인 ID를 설정한다.
     * Args:
     *  - id: 라인 ID
     * Returns: 없음
     * Side Effects: 없음
     * Raises: 없음
     */
    public void setId(Long id) {
        this.id = id;
    }

    /**
     * 목적: 주문을 반환한다.
     * Args: 없음
     * Returns:
     *  - Order: 주문
     * Side Effects: 없음
     * Raises: 없음
     */
    public Order getOrder() {
        return order;
    }

    /**
     * 목적: 주문을 설정한다.
     * Args:
     *  - order: 주문
     * Returns: 없음
     * Side Effects: 없음
     * Raises: 없음
     */
    public void setOrder(Order order) {
        this.order = order;
    }

    /**
     * 목적: 품목을 반환한다.
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
     * 목적: 품목을 설정한다.
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
}
