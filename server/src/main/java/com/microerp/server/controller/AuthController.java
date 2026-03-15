package com.microerp.server.controller;

import com.microerp.server.dto.AuthResponse;
import com.microerp.server.dto.CurrentUserResponse;
import com.microerp.server.dto.LoginRequest;
import com.microerp.server.service.AuthService;
import jakarta.validation.Valid;
import java.util.List;
import org.springframework.http.ResponseEntity;
import org.springframework.security.core.Authentication;
import org.springframework.security.core.GrantedAuthority;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping("/api/auth")
public class AuthController {
    private final AuthService authService;

    public AuthController(AuthService authService) {
        this.authService = authService;
    }

    @PostMapping("/login")
    public ResponseEntity<AuthResponse> login(@Valid @RequestBody LoginRequest request) {
        return ResponseEntity.ok(authService.login(request));
    }

    @GetMapping("/me")
    public ResponseEntity<CurrentUserResponse> me(Authentication authentication) {
        String username = authentication.getName();
        List<String> authorities = authentication.getAuthorities().stream()
            .map(GrantedAuthority::getAuthority)
            .toList();

        String role = authorities.stream()
            .filter(value -> value.startsWith("ROLE_"))
            .findFirst()
            .map(value -> value.replace("ROLE_", ""))
            .orElse("STAFF");

        List<String> scopes = authorities.stream()
            .filter(value -> value.startsWith("SCOPE_"))
            .map(value -> value.replace("SCOPE_", ""))
            .toList();

        return ResponseEntity.ok(new CurrentUserResponse(username, role, scopes));
    }
}
