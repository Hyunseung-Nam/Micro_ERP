package com.microerp.server.exception;

import org.springframework.http.HttpStatus;

/**
 * 역할: API 레벨 오류를 표현한다.
 * 책임: HTTP 상태와 메시지 보관.
 * 외부 의존성: Spring Web HttpStatus.
 */
public class ApiException extends RuntimeException {
    private final HttpStatus status;

    /**
     * 목적: API 예외를 생성한다.
     * Args:
     *  - status: HTTP 상태
     *  - message: 오류 메시지
     * Returns: 없음
     * Side Effects: 없음
     * Raises: 없음
     */
    public ApiException(HttpStatus status, String message) {
        super(message);
        this.status = status;
    }

    /**
     * 목적: HTTP 상태를 반환한다.
     * Args: 없음
     * Returns:
     *  - HttpStatus: 상태 코드
     * Side Effects: 없음
     * Raises: 없음
     */
    public HttpStatus getStatus() {
        return status;
    }
}
