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

@Component
public class JwtAuthenticationFilter extends OncePerRequestFilter {
    private static final Logger logger = LoggerFactory.getLogger(JwtAuthenticationFilter.class);

    private final JwtService jwtService;

    public JwtAuthenticationFilter(JwtService jwtService) {
        this.jwtService = jwtService;
    }

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
                List<SimpleGrantedAuthority> authorities = jwtService.extractAuthorities(jwt).stream()
                    .map(SimpleGrantedAuthority::new)
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
