package com.microerp.server.dto;

import java.time.Instant;

/**
 * 역할: 사용자 조회 응답을 표현한다.
 * 책임: 사용자 식별자와 권한 정보를 제공.
 * 외부 의존성: Java Time.
 */
public class UserResponse {
    private String username;
    private String role;
    private Instant createdAt;

    /**
     * 목적: 기본 생성자.
     * Args: 없음
     * Returns: 없음
     * Side Effects: 없음
     * Raises: 없음
     */
    public UserResponse() {
    }

    /**
     * 목적: 사용자 응답을 생성한다.
     * Args:
     *  - username: 사용자명
     *  - role: 권한
     *  - createdAt: 생성 시각
     * Returns: 없음
     * Side Effects: 없음
     * Raises: 없음
     */
    public UserResponse(String username, String role, Instant createdAt) {
        this.username = username;
        this.role = role;
        this.createdAt = createdAt;
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
}
