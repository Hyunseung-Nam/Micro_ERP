package com.microerp.server.dto;

/**
 * 역할: 인증 응답을 표현한다.
 * 책임: 토큰과 사용자 정보를 전달.
 * 외부 의존성: 없음.
 */
public class AuthResponse {
    private String token;
    private String username;
    private String role;

    /**
     * 목적: 기본 생성자.
     * Args: 없음
     * Returns: 없음
     * Side Effects: 없음
     * Raises: 없음
     */
    public AuthResponse() {
    }

    /**
     * 목적: 인증 응답을 생성한다.
     * Args:
     *  - token: JWT 토큰
     *  - username: 사용자명
     *  - role: 권한
     * Returns: 없음
     * Side Effects: 없음
     * Raises: 없음
     */
    public AuthResponse(String token, String username, String role) {
        this.token = token;
        this.username = username;
        this.role = role;
    }

    /**
     * 목적: 토큰을 반환한다.
     * Args: 없음
     * Returns:
     *  - String: JWT 토큰
     * Side Effects: 없음
     * Raises: 없음
     */
    public String getToken() {
        return token;
    }

    /**
     * 목적: 토큰을 설정한다.
     * Args:
     *  - token: JWT 토큰
     * Returns: 없음
     * Side Effects: 없음
     * Raises: 없음
     */
    public void setToken(String token) {
        this.token = token;
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
     * 목적: 권한을 반환한다.
     * Args: 없음
     * Returns:
     *  - String: 권한
     * Side Effects: 없음
     * Raises: 없음
     */
    public String getRole() {
        return role;
    }

    /**
     * 목적: 권한을 설정한다.
     * Args:
     *  - role: 권한
     * Returns: 없음
     * Side Effects: 없음
     * Raises: 없음
     */
    public void setRole(String role) {
        this.role = role;
    }
}
