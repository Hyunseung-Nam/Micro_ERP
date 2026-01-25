package com.microerp.server.dto;

import jakarta.validation.constraints.NotBlank;

/**
 * 역할: 로그인 요청 데이터를 표현한다.
 * 책임: 사용자명과 비밀번호 전달.
 * 외부 의존성: Bean Validation.
 */
public class LoginRequest {
    @NotBlank
    private String username;

    @NotBlank
    private String password;

    /**
     * 목적: 기본 생성자.
     * Args: 없음
     * Returns: 없음
     * Side Effects: 없음
     * Raises: 없음
     */
    public LoginRequest() {
    }

    /**
     * 목적: 사용자명을 반환한다.
     * Args: 없음
     * Returns:
     *  - String: 사용자명
     * Side Effects: 없음
     * Raises: 없음
     */
    public String getUsername() {
        return username;
    }

    /**
     * 목적: 사용자명을 설정한다.
     * Args:
     *  - username: 사용자명
     * Returns: 없음
     * Side Effects: 없음
     * Raises: 없음
     */
    public void setUsername(String username) {
        this.username = username;
    }

    /**
     * 목적: 비밀번호를 반환한다.
     * Args: 없음
     * Returns:
     *  - String: 비밀번호
     * Side Effects: 없음
     * Raises: 없음
     */
    public String getPassword() {
        return password;
    }

    /**
     * 목적: 비밀번호를 설정한다.
     * Args:
     *  - password: 비밀번호
     * Returns: 없음
     * Side Effects: 없음
     * Raises: 없음
     */
    public void setPassword(String password) {
        this.password = password;
    }
}
