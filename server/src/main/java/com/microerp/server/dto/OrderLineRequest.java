package com.microerp.server.dto;

import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.NotNull;

/**
 * 역할: 발주 라인 요청을 표현한다.
 * 책임: 품목, 수량, 단위 전달.
 * 외부 의존성: Bean Validation.
 */
public class OrderLineRequest {
    @NotBlank
    private String itemId;

    @NotNull
    private Integer quantity;

    @NotBlank
    private String unit;

    /**
     * 목적: 기본 생성자.
     * Args: 없음
     * Returns: 없음
     * Side Effects: 없음
     * Raises: 없음
     */
    public OrderLineRequest() {
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
     * 목적: 수량을 반환한다.
     * Args: 없음
     * Returns:
     *  - Integer: 수량
     * Side Effects: 없음
     * Raises: 없음
     */
    public Integer getQuantity() {
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
    public void setQuantity(Integer quantity) {
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
