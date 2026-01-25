package com.microerp.server.domain;

import jakarta.persistence.Column;
import jakarta.persistence.Entity;
import jakarta.persistence.Id;
import jakarta.persistence.Table;
import java.time.Instant;

/**
 * 역할: 사용자 계정 정보를 표현한다.
 * 책임: 로그인 식별자, 해시 비밀번호, 권한 보관.
 * 외부 의존성: JPA.
 */
@Entity
@Table(name = "users")
public class User {
    @Id
    @Column(name = "username", nullable = false, length = 50)
    private String username;

    @Column(name = "password_hash", nullable = false, length = 255)
    private String passwordHash;

    @Column(name = "role", nullable = false, length = 30)
    private String role;

    @Column(name = "created_at", nullable = false)
    private Instant createdAt;

    /**
     * 목적: JPA 기본 생성자.
     * Args: 없음
     * Returns: 없음
     * Side Effects: 없음
     * Raises: 없음
     */
    public User() {
        this.createdAt = Instant.now();
    }

    /**
     * 목적: 사용자 객체를 생성한다.
     * Args:
     *  - username: 사용자명
     *  - passwordHash: 해시 비밀번호
     *  - role: 권한
     * Returns: 없음
     * Side Effects: 없음
     * Raises: 없음
     */
    public User(String username, String passwordHash, String role) {
        this.username = username;
        this.passwordHash = passwordHash;
        this.role = role;
        this.createdAt = Instant.now();
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
     * 목적: 비밀번호 해시를 반환한다.
     * Args: 없음
     * Returns:
     *  - String: 비밀번호 해시
     * Side Effects: 없음
     * Raises: 없음
     */
    public String getPasswordHash() {
        return passwordHash;
    }

    /**
     * 목적: 비밀번호 해시를 설정한다.
     * Args:
     *  - passwordHash: 해시 비밀번호
     * Returns: 없음
     * Side Effects: 없음
     * Raises: 없음
     */
    public void setPasswordHash(String passwordHash) {
        this.passwordHash = passwordHash;
    }

    /**
     * 목적: 사용자 권한을 반환한다.
     * Args: 없음
     * Returns:
     *  - String: 권한 문자열
     * Side Effects: 없음
     * Raises: 없음
     */
    public String getRole() {
        return role;
    }

    /**
     * 목적: 사용자 권한을 설정한다.
     * Args:
     *  - role: 권한 문자열
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
