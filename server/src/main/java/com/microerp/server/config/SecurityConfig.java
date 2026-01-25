package com.microerp.server.config;

import com.microerp.server.security.JwtAuthenticationFilter;
import com.microerp.server.security.JwtService;
import com.nimbusds.jose.jwk.source.ImmutableSecret;
import com.nimbusds.jose.proc.SecurityContext;
import javax.crypto.SecretKey;
import javax.crypto.spec.SecretKeySpec;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.boot.autoconfigure.security.servlet.PathRequest;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.http.HttpMethod;
import org.springframework.security.config.Customizer;
import org.springframework.security.config.annotation.web.builders.HttpSecurity;
import org.springframework.security.config.http.SessionCreationPolicy;
import org.springframework.security.crypto.bcrypt.BCryptPasswordEncoder;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.security.oauth2.jose.jws.MacAlgorithm;
import org.springframework.security.oauth2.jwt.JwtDecoder;
import org.springframework.security.oauth2.jwt.JwtEncoder;
import org.springframework.security.oauth2.jwt.NimbusJwtDecoder;
import org.springframework.security.oauth2.jwt.NimbusJwtEncoder;
import org.springframework.security.web.SecurityFilterChain;
import org.springframework.security.web.authentication.UsernamePasswordAuthenticationFilter;

/**
 * 역할: JWT 기반 인증/인가 설정을 담당한다.
 * 책임: 보안 필터 체인 구성, 암호화 키 및 인코더 구성.
 * 외부 의존성: Spring Security, Nimbus JOSE.
 */
@Configuration
public class SecurityConfig {
    /**
     * 목적: 보안 필터 체인을 구성한다.
     * Args:
     *  - http: HttpSecurity 구성자
     * Returns:
     *  - SecurityFilterChain: 보안 체인
     * Side Effects:
     *  - 요청 인증/인가 정책을 등록한다.
     * Raises:
     *  - Exception: 보안 구성이 실패할 경우
     */
    @Bean
    public SecurityFilterChain securityFilterChain(
            HttpSecurity http,
            JwtAuthenticationFilter jwtAuthenticationFilter
    ) throws Exception {
        http
            .csrf(csrf -> csrf.disable())
            .sessionManagement(session -> session.sessionCreationPolicy(SessionCreationPolicy.STATELESS))
            .authorizeHttpRequests(auth -> auth
                .requestMatchers(HttpMethod.POST, "/api/auth/login").permitAll()
                .requestMatchers(HttpMethod.GET, "/", "/index.html", "/dashboard.html", "/error").permitAll()
                .requestMatchers(PathRequest.toStaticResources().atCommonLocations()).permitAll()
                .requestMatchers("/actuator/**").permitAll()
                .anyRequest().authenticated()
            )
            .httpBasic(httpBasic -> httpBasic.disable())
            .formLogin(form -> form.disable());

        http.addFilterBefore(jwtAuthenticationFilter, UsernamePasswordAuthenticationFilter.class);
        return http.build();
    }

    /**
     * 목적: 비밀번호 인코더를 제공한다.
     * Args: 없음
     * Returns:
     *  - PasswordEncoder: BCrypt 기반 인코더
     * Side Effects: 없음
     * Raises: 없음
     */
    @Bean
    public PasswordEncoder passwordEncoder() {
        return new BCryptPasswordEncoder();
    }

    /**
     * 목적: JWT 인코더를 생성한다.
     * Args:
     *  - secret: JWT 서명용 시크릿
     * Returns:
     *  - JwtEncoder: HMAC 기반 인코더
     * Side Effects: 없음
     * Raises: 없음
     */
    @Bean
    public JwtEncoder jwtEncoder(@Value("${app.jwt.secret}") String secret) {
        SecretKey secretKey = new SecretKeySpec(secret.getBytes(), "HmacSHA256");
        return new NimbusJwtEncoder(new ImmutableSecret<SecurityContext>(secretKey));
    }

    /**
     * 목적: JWT 디코더를 생성한다.
     * Args:
     *  - secret: JWT 서명용 시크릿
     * Returns:
     *  - JwtDecoder: HMAC 기반 디코더
     * Side Effects: 없음
     * Raises: 없음
     */
    @Bean
    public JwtDecoder jwtDecoder(@Value("${app.jwt.secret}") String secret) {
        SecretKey secretKey = new SecretKeySpec(secret.getBytes(), "HmacSHA256");
        return NimbusJwtDecoder.withSecretKey(secretKey).macAlgorithm(MacAlgorithm.HS256).build();
    }
}
