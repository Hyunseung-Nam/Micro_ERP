package com.microerp.server.dto;

import jakarta.validation.Valid;
import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.NotEmpty;
import java.util.ArrayList;
import java.util.List;

/**
 * 역할: 발주 생성 요청을 표현한다.
 * 책임: 거래처와 라인 정보를 전달.
 * 외부 의존성: Bean Validation.
 */
public class OrderCreateRequest {
    @NotBlank
    private String partnerId;

    @Valid
    @NotEmpty
    private List<OrderLineRequest> lines = new ArrayList<>();

    /**
     * 목적: 기본 생성자.
     * Args: 없음
     * Returns: 없음
     * Side Effects: 없음
     * Raises: 없음
     */
    public OrderCreateRequest() {
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
     * 목적: 발주 라인 목록을 반환한다.
     * Args: 없음
     * Returns:
     *  - List<OrderLineRequest>: 라인 목록
     * Side Effects: 없음
     * Raises: 없음
     */
    public List<OrderLineRequest> getLines() {
        return lines;
    }

    /**
     * 목적: 발주 라인 목록을 설정한다.
     * Args:
     *  - lines: 라인 목록
     * Returns: 없음
     * Side Effects: 없음
     * Raises: 없음
     */
    public void setLines(List<OrderLineRequest> lines) {
        this.lines = lines;
    }
}
