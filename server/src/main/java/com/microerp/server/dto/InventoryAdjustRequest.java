package com.microerp.server.dto;

import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.NotNull;

/**
 * 역할: 재고 조정 요청을 표현한다.
 * 책임: 품목, 위치, 수량 변동 정보 전달.
 * 외부 의존성: Bean Validation.
 */
public class InventoryAdjustRequest {
    @NotBlank
    private String itemId;

    @NotBlank
    private String locationId;

    @NotNull
    private Integer deltaQuantity;

    /**
     * 목적: 기본 생성자.
     * Args: 없음
     * Returns: 없음
     * Side Effects: 없음
     * Raises: 없음
     */
    public InventoryAdjustRequest() {
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
     * 목적: 수량 변동을 반환한다.
     * Args: 없음
     * Returns:
     *  - Integer: 변동 수량
     * Side Effects: 없음
     * Raises: 없음
     */
    public Integer getDeltaQuantity() {
        return deltaQuantity;
    }

    /**
     * 목적: 수량 변동을 설정한다.
     * Args:
     *  - deltaQuantity: 변동 수량
     * Returns: 없음
     * Side Effects: 없음
     * Raises: 없음
     */
    public void setDeltaQuantity(Integer deltaQuantity) {
        this.deltaQuantity = deltaQuantity;
    }
}
