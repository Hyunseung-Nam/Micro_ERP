package com.microerp.server.dto;

/**
 * 역할: 재고 조회 응답 항목을 표현한다.
 * 책임: 품목/위치/수량 정보를 제공.
 * 외부 의존성: 없음.
 */
public class InventoryItemResponse {
    private String itemId;
    private String itemName;
    private String unit;
    private int safetyStock;
    private String locationId;
    private String locationName;
    private int quantity;

    /**
     * 목적: 기본 생성자.
     * Args: 없음
     * Returns: 없음
     * Side Effects: 없음
     * Raises: 없음
     */
    public InventoryItemResponse() {
    }

    /**
     * 목적: 재고 응답 항목을 생성한다.
     * Args:
     *  - itemId: 품목 ID
     *  - itemName: 품목명
     *  - unit: 단위
     *  - safetyStock: 안전재고
     *  - locationId: 위치 ID
     *  - locationName: 위치명
     *  - quantity: 수량
     * Returns: 없음
     * Side Effects: 없음
     * Raises: 없음
     */
    public InventoryItemResponse(
            String itemId,
            String itemName,
            String unit,
            int safetyStock,
            String locationId,
            String locationName,
            int quantity
    ) {
        this.itemId = itemId;
        this.itemName = itemName;
        this.unit = unit;
        this.safetyStock = safetyStock;
        this.locationId = locationId;
        this.locationName = locationName;
        this.quantity = quantity;
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
    public String getLocationName() {
        return locationName;
    }

    /**
     * 목적: 위치명을 설정한다.
     * Args:
     *  - locationName: 위치명
     * Returns: 없음
     * Side Effects: 없음
     * Raises: 없음
     */
    public void setLocationName(String locationName) {
        this.locationName = locationName;
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
