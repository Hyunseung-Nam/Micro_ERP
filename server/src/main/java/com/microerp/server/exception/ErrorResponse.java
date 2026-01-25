package com.microerp.server.exception;

import java.time.Instant;

/**
 * 역할: API 오류 응답 페이로드를 정의한다.
 * 책임: 오류 메시지, 코드, 시간 보관.
 * 외부 의존성: Java Time.
 */
public class ErrorResponse {
    private final String message;
    private final String code;
    private final Instant timestamp;

    /**
     * 목적: 오류 응답을 생성한다.
     * Args:
     *  - message: 오류 메시지
     *  - code: 오류 코드
     * Returns: 없음
     * Side Effects: 없음
     * Raises: 없음
     */
    public ErrorResponse(String message, String code) {
        this.message = message;
        this.code = code;
        this.timestamp = Instant.now();
    }

    /**
     * 목적: 오류 메시지를 반환한다.
     * Args: 없음
     * Returns:
     *  - String: 오류 메시지
     * Side Effects: 없음
     * Raises: 없음
     */
    public String getMessage() {
        return message;
    }

    /**
     * 목적: 오류 코드를 반환한다.
     * Args: 없음
     * Returns:
     *  - String: 오류 코드
     * Side Effects: 없음
     * Raises: 없음
     */
    public String getCode() {
        return code;
    }

    /**
     * 목적: 오류 발생 시각을 반환한다.
     * Args: 없음
     * Returns:
     *  - Instant: 오류 시각
     * Side Effects: 없음
     * Raises: 없음
     */
    public Instant getTimestamp() {
        return timestamp;
    }
}
