package com.microerp.server.security;

import jakarta.servlet.FilterChain;
import jakarta.servlet.ServletException;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpServletResponse;
import java.io.IOException;
import java.util.List;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.security.authentication.UsernamePasswordAuthenticationToken;
import org.springframework.security.core.authority.SimpleGrantedAuthority;
import org.springframework.security.core.context.SecurityContextHolder;
import org.springframework.security.oauth2.jwt.Jwt;
import org.springframework.stereotype.Component;
import org.springframework.web.filter.OncePerRequestFilter;

/**
 * 역할: 요청 헤더의 JWT를 검증하고 인증 정보를 등록한다.
 * 책임: Authorization 헤더 처리, SecurityContext 등록.
 * 외부 의존성: Servlet API, Spring Security.
 */
@Component
public class JwtAuthenticationFilter extends OncePerRequestFilter {
    private static final Logger logger = LoggerFactory.getLogger(JwtAuthenticationFilter.class);

    private final JwtService jwtService;

    public JwtAuthenticationFilter(JwtService jwtService) {
        this.jwtService = jwtService;
    }

    /**
     * 목적: 요청에서 JWT를 추출해 인증 정보를 설정한다.
     * Args:
     *  - request: HTTP 요청
     *  - response: HTTP 응답
     *  - filterChain: 다음 필터 체인
     * Returns:
     *  - void
     * Side Effects:
     *  - SecurityContext에 인증 정보를 설정한다.
     * Raises:
     *  - IOException, ServletException: 필터 처리 실패 시
     */
    @Override
    protected void doFilterInternal(
            HttpServletRequest request,
            HttpServletResponse response,
            FilterChain filterChain
    ) throws ServletException, IOException {
        String authorization = request.getHeader("Authorization");
        if (authorization != null && authorization.startsWith("Bearer ")) {
            String token = authorization.substring("Bearer ".length());
            try {
                Jwt jwt = jwtService.decode(token);
                List<SimpleGrantedAuthority> authorities = jwtService.extractRoles(jwt).stream()
                    .map(role -> new SimpleGrantedAuthority("ROLE_" + role))
                    .toList();
                UsernamePasswordAuthenticationToken authToken =
                    new UsernamePasswordAuthenticationToken(jwt.getSubject(), null, authorities);
                SecurityContextHolder.getContext().setAuthentication(authToken);
            } catch (RuntimeException ex) {
                logger.warn("Invalid JWT token: {}", ex.getMessage());
            }
        }

        filterChain.doFilter(request, response);
    }
}
