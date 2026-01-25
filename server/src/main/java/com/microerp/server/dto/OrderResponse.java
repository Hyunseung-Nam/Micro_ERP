package com.microerp.server.dto;

import java.time.Instant;
import java.util.ArrayList;
import java.util.List;

/**
 * 역할: 발주 응답을 표현한다.
 * 책임: 발주 상태와 라인 정보를 제공.
 * 외부 의존성: Java Time.
 */
public class OrderResponse {
    private Long orderId;
    private String partnerId;
    private String partnerName;
    private String status;
    private Instant createdAt;
    private List<OrderLineResponse> lines = new ArrayList<>();

    /**
     * 목적: 기본 생성자.
     * Args: 없음
     * Returns: 없음
     * Side Effects: 없음
     * Raises: 없음
     */
    public OrderResponse() {
    }

    /**
     * 목적: 발주 응답을 생성한다.
     * Args:
     *  - orderId: 발주 ID
     *  - partnerId: 거래처 ID
     *  - partnerName: 거래처명
     *  - status: 상태
     *  - createdAt: 생성 시각
     *  - lines: 라인 목록
     * Returns: 없음
     * Side Effects: 없음
     * Raises: 없음
     */
    public OrderResponse(
            Long orderId,
            String partnerId,
            String partnerName,
            String status,
            Instant createdAt,
            List<OrderLineResponse> lines
    ) {
        this.orderId = orderId;
        this.partnerId = partnerId;
        this.partnerName = partnerName;
        this.status = status;
        this.createdAt = createdAt;
        this.lines = lines;
    }

    /**
     * 목적: 발주 ID를 반환한다.
     * Args: 없음
     * Returns:
     *  - Long: 발주 ID
     * Side Effects: 없음
     * Raises: 없음
     */
    public Long getOrderId() {
        return orderId;
    }

    /**
     * 목적: 발주 ID를 설정한다.
     * Args:
     *  - orderId: 발주 ID
     * Returns: 없음
     * Side Effects: 없음
     * Raises: 없음
     */
    public void setOrderId(Long orderId) {
        this.orderId = orderId;
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
    public String getPartnerName() {
        return partnerName;
    }

    /**
     * 목적: 거래처명을 설정한다.
     * Args:
     *  - partnerName: 거래처명
     * Returns: 없음
     * Side Effects: 없음
     * Raises: 없음
     */
    public void setPartnerName(String partnerName) {
        this.partnerName = partnerName;
    }

    /**
     * 목적: 상태를 반환한다.
     * Args: 없음
     * Returns:
     *  - String: 상태
     * Side Effects: 없음
     * Raises: 없음
     */
    public String getStatus() {
        return status;
    }

    /**
     * 목적: 상태를 설정한다.
     * Args:
     *  - status: 상태
     * Returns: 없음
     * Side Effects: 없음
     * Raises: 없음
     */
    public void setStatus(String status) {
        this.status = status;
    }

    /**
     * 목적: 생성 시각을 반환한다.
     * Args: 없음
     * Returns:
     *  - Instant: 생성 시각
     * Side Effects: 없음
     * Raises: 없음
     */
    public Instant getCreatedAt() {
        return createdAt;
    }

    /**
     * 목적: 생성 시각을 설정한다.
     * Args:
     *  - createdAt: 생성 시각
     * Returns: 없음
     * Side Effects: 없음
     * Raises: 없음
     */
    public void setCreatedAt(Instant createdAt) {
        this.createdAt = createdAt;
    }

    /**
     * 목적: 라인 목록을 반환한다.
     * Args: 없음
     * Returns:
     *  - List<OrderLineResponse>: 라인 목록
     * Side Effects: 없음
     * Raises: 없음
     */
    public List<OrderLineResponse> getLines() {
        return lines;
    }

    /**
     * 목적: 라인 목록을 설정한다.
     * Args:
     *  - lines: 라인 목록
     * Returns: 없음
     * Side Effects: 없음
     * Raises: 없음
     */
    public void setLines(List<OrderLineResponse> lines) {
        this.lines = lines;
    }
}
