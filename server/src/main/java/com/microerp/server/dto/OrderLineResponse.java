package com.microerp.server.dto;

/**
 * 역할: 발주 라인 응답을 표현한다.
 * 책임: 품목, 수량, 단위 전달.
 * 외부 의존성: 없음.
 */
public class OrderLineResponse {
    private String itemId;
    private String itemName;
    private int quantity;
    private String unit;

    /**
     * 목적: 기본 생성자.
     * Args: 없음
     * Returns: 없음
     * Side Effects: 없음
     * Raises: 없음
     */
    public OrderLineResponse() {
    }

    /**
     * 목적: 발주 라인 응답을 생성한다.
     * Args:
     *  - itemId: 품목 ID
     *  - itemName: 품목명
     *  - quantity: 수량
     *  - unit: 단위
     * Returns: 없음
     * Side Effects: 없음
     * Raises: 없음
     */
    public OrderLineResponse(String itemId, String itemName, int quantity, String unit) {
        this.itemId = itemId;
        this.itemName = itemName;
        this.quantity = quantity;
        this.unit = unit;
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
    public String getItemName() {
        return itemName;
    }

    /**
     * 목적: 품목명을 설정한다.
     * Args:
     *  - itemName: 품목명
     * Returns: 없음
     * Side Effects: 없음
     * Raises: 없음
     */
    public void setItemName(String itemName) {
        this.itemName = itemName;
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
