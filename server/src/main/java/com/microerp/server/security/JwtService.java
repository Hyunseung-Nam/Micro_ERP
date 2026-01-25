package com.microerp.server.security;

import com.microerp.server.domain.User;
import java.time.Instant;
import java.util.List;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.security.oauth2.jwt.Jwt;
import org.springframework.security.oauth2.jwt.JwtClaimsSet;
import org.springframework.security.oauth2.jwt.JwtDecoder;
import org.springframework.security.oauth2.jwt.JwtEncoder;
import org.springframework.security.oauth2.jwt.JwtEncoderParameters;
import org.springframework.security.oauth2.jwt.JwsHeader;
import org.springframework.stereotype.Service;
import org.springframework.security.oauth2.jose.jws.MacAlgorithm;

/**
 * 역할: JWT 생성 및 검증을 담당한다.
 * 책임: 토큰 발급/디코딩 로직 제공.
 * 외부 의존성: Spring Security JWT.
 */
@Service
public class JwtService {
    private static final Logger logger = LoggerFactory.getLogger(JwtService.class);

    private final JwtEncoder jwtEncoder;
    private final JwtDecoder jwtDecoder;
    private final String issuer;
    private final long ttlMinutes;

    public JwtService(
            JwtEncoder jwtEncoder,
            JwtDecoder jwtDecoder,
            @Value("${app.jwt.issuer}") String issuer,
            @Value("${app.jwt.ttl-minutes}") long ttlMinutes
    ) {
        this.jwtEncoder = jwtEncoder;
        this.jwtDecoder = jwtDecoder;
        this.issuer = issuer;
        this.ttlMinutes = ttlMinutes;
    }

    /**
     * 목적: 사용자 정보를 기반으로 JWT를 발급한다.
     * Args:
     *  - user: 인증된 사용자
     * Returns:
     *  - String: JWT 토큰
     * Side Effects:
     *  - 토큰 발급 로그를 남긴다.
     * Raises:
     *  - RuntimeException: 인코딩 실패 시
     */
    public String generateToken(User user) {
        Instant now = Instant.now();
        JwsHeader headers = JwsHeader.with(MacAlgorithm.HS256).build();
        JwtClaimsSet claims = JwtClaimsSet.builder()
            .issuer(issuer)
            .issuedAt(now)
            .expiresAt(now.plusSeconds(ttlMinutes * 60))
            .subject(user.getUsername())
            .claim("role", user.getRole())
            .build();

        logger.info("Issuing JWT for user {}", user.getUsername());
        return jwtEncoder.encode(JwtEncoderParameters.from(headers, claims)).getTokenValue();
    }

    /**
     * 목적: JWT를 디코딩한다.
     * Args:
     *  - token: JWT 토큰 문자열
     * Returns:
     *  - Jwt: 디코딩된 JWT
     * Side Effects: 없음
     * Raises:
     *  - RuntimeException: 디코딩 실패 시
     */
    public Jwt decode(String token) {
        return jwtDecoder.decode(token);
    }

    /**
     * 목적: JWT에서 권한 문자열을 추출한다.
     * Args:
     *  - jwt: 디코딩된 JWT
     * Returns:
     *  - List<String>: 권한 문자열 목록
     * Side Effects: 없음
     * Raises: 없음
     */
    public List<String> extractRoles(Jwt jwt) {
        Object role = jwt.getClaims().get("role");
        if (role == null) {
            return List.of();
        }
        return List.of(role.toString());
    }
}
