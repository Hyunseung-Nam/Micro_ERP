package com.microerp.server.security;

import com.microerp.server.domain.User;
import com.microerp.server.service.RbacService;
import java.time.Instant;
import java.util.ArrayList;
import java.util.List;
import java.util.Set;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.security.oauth2.jose.jws.MacAlgorithm;
import org.springframework.security.oauth2.jwt.Jwt;
import org.springframework.security.oauth2.jwt.JwtClaimsSet;
import org.springframework.security.oauth2.jwt.JwtDecoder;
import org.springframework.security.oauth2.jwt.JwtEncoder;
import org.springframework.security.oauth2.jwt.JwtEncoderParameters;
import org.springframework.security.oauth2.jwt.JwsHeader;
import org.springframework.stereotype.Service;

@Service
public class JwtService {
    private static final Logger logger = LoggerFactory.getLogger(JwtService.class);

    private final JwtEncoder jwtEncoder;
    private final JwtDecoder jwtDecoder;
    private final String issuer;
    private final long ttlMinutes;
    private final RbacService rbacService;

    public JwtService(
            JwtEncoder jwtEncoder,
            JwtDecoder jwtDecoder,
            @Value("${app.jwt.issuer}") String issuer,
            @Value("${app.jwt.ttl-minutes}") long ttlMinutes,
            RbacService rbacService
    ) {
        this.jwtEncoder = jwtEncoder;
        this.jwtDecoder = jwtDecoder;
        this.issuer = issuer;
        this.ttlMinutes = ttlMinutes;
        this.rbacService = rbacService;
    }

    public String generateToken(User user) {
        Instant now = Instant.now();
        String role = user.getRole() == null ? "STAFF" : user.getRole().trim().toUpperCase();
        Set<String> scopes = rbacService.scopesForRole(role);

        JwsHeader headers = JwsHeader.with(MacAlgorithm.HS256).build();
        JwtClaimsSet claims = JwtClaimsSet.builder()
            .issuer(issuer)
            .issuedAt(now)
            .expiresAt(now.plusSeconds(ttlMinutes * 60))
            .subject(user.getUsername())
            .claim("role", role)
            .claim("scopes", scopes)
            .build();

        logger.info("Issuing JWT for user {}", user.getUsername());
        return jwtEncoder.encode(JwtEncoderParameters.from(headers, claims)).getTokenValue();
    }

    public Jwt decode(String token) {
        return jwtDecoder.decode(token);
    }

    public List<String> extractAuthorities(Jwt jwt) {
        List<String> authorities = new ArrayList<>();

        Object role = jwt.getClaims().get("role");
        if (role != null) {
            authorities.add("ROLE_" + role.toString().toUpperCase());
        }

        Object scopes = jwt.getClaims().get("scopes");
        if (scopes instanceof Iterable<?> iterable) {
            for (Object scope : iterable) {
                if (scope != null && !"*".equals(scope.toString())) {
                    authorities.add("SCOPE_" + scope.toString());
                }
            }
        }
        return authorities;
    }
}
