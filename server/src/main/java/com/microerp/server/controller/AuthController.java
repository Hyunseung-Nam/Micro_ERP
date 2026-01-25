package com.microerp.server.controller;

import com.microerp.server.dto.AuthResponse;
import com.microerp.server.dto.CurrentUserResponse;
import com.microerp.server.dto.LoginRequest;
import com.microerp.server.service.AuthService;
import jakarta.validation.Valid;
import java.util.Optional;
import org.springframework.http.ResponseEntity;
import org.springframework.security.core.Authentication;
import org.springframework.security.core.GrantedAuthority;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

/**
 * 역할: 인증 관련 API를 제공한다.
 * 책임: 로그인 및 현재 사용자 정보 제공.
 * 외부 의존성: Spring Web, Spring Security.
 */
@RestController
@RequestMapping("/api/auth")
public class AuthController {
    private final AuthService authService;

    public AuthController(AuthService authService) {
        this.authService = authService;
    }

    /**
     * 목적: 로그인 요청을 처리한다.
     * Args:
     *  - request: 로그인 요청
     * Returns:
     *  - ResponseEntity<AuthResponse>: 인증 결과
     * Side Effects: 없음
     * Raises: 없음
     */
    @PostMapping("/login")
    public ResponseEntity<AuthResponse> login(@Valid @RequestBody LoginRequest request) {
        return ResponseEntity.ok(authService.login(request));
    }

    /**
     * 목적: 현재 사용자 정보를 반환한다.
     * Args:
     *  - authentication: 인증 정보
     * Returns:
     *  - ResponseEntity<CurrentUserResponse>: 현재 사용자 정보
     * Side Effects: 없음
     * Raises: 없음
     */
    @GetMapping("/me")
    public ResponseEntity<CurrentUserResponse> me(Authentication authentication) {
        String username = authentication.getName();
        Optional<? extends GrantedAuthority> authority = authentication.getAuthorities().stream().findFirst();
        String role = authority.map(GrantedAuthority::getAuthority).orElse("ROLE_USER");
        role = role.replace("ROLE_", "");
        return ResponseEntity.ok(new CurrentUserResponse(username, role));
    }
}
