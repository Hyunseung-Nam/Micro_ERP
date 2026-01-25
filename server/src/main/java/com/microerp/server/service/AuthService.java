package com.microerp.server.service;

import com.microerp.server.domain.User;
import com.microerp.server.dto.AuthResponse;
import com.microerp.server.dto.LoginRequest;
import com.microerp.server.exception.ApiException;
import com.microerp.server.repository.UserRepository;
import com.microerp.server.security.JwtService;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.dao.DataAccessException;
import org.springframework.http.HttpStatus;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.stereotype.Service;

/**
 * 역할: 로그인 인증 로직을 제공한다.
 * 책임: 사용자 검증 및 JWT 발급.
 * 외부 의존성: Spring Data JPA, Spring Security.
 */
@Service
public class AuthService {
    private static final Logger logger = LoggerFactory.getLogger(AuthService.class);

    private final UserRepository userRepository;
    private final PasswordEncoder passwordEncoder;
    private final JwtService jwtService;

    public AuthService(
            UserRepository userRepository,
            PasswordEncoder passwordEncoder,
            JwtService jwtService
    ) {
        this.userRepository = userRepository;
        this.passwordEncoder = passwordEncoder;
        this.jwtService = jwtService;
    }

    /**
     * 목적: 로그인 요청을 검증하고 토큰을 발급한다.
     * Args:
     *  - request: 로그인 요청
     * Returns:
     *  - AuthResponse: 인증 응답
     * Side Effects:
     *  - 인증 로그를 기록한다.
     * Raises:
     *  - ApiException: 인증 실패 또는 DB 오류 발생 시
     */
    public AuthResponse login(LoginRequest request) {
        try {
            User user = userRepository.findById(request.getUsername())
                .orElseThrow(() -> new ApiException(HttpStatus.UNAUTHORIZED, "Invalid credentials"));

            if (!passwordEncoder.matches(request.getPassword(), user.getPasswordHash())) {
                throw new ApiException(HttpStatus.UNAUTHORIZED, "Invalid credentials");
            }

            String token = jwtService.generateToken(user);
            logger.info("User {} authenticated", user.getUsername());
            return new AuthResponse(token, user.getUsername(), user.getRole());
        } catch (DataAccessException ex) {
            logger.error("Database error during login", ex);
            throw new ApiException(HttpStatus.INTERNAL_SERVER_ERROR, "Database error");
        }
    }
}
