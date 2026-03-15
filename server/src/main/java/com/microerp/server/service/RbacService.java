package com.microerp.server.service;

import java.util.LinkedHashSet;
import java.util.Set;
import org.springframework.stereotype.Service;

@Service("rbacService")
public class RbacService {
    public Set<String> scopesForRole(String role) {
        String normalized = role == null ? "STAFF" : role.trim().toUpperCase();
        return switch (normalized) {
            case "ADMIN" -> Set.of("*");
            case "MANAGER" -> Set.of(
                "inventory.read", "inventory.adjust",
                "order.read", "order.create", "order.close",
                "approval.read", "approval.request", "approval.approve", "approval.reject",
                "workflow.hospital.consume", "workflow.ecommerce.exchange",
                "audit.read"
            );
            case "AUDITOR" -> Set.of("inventory.read", "order.read", "approval.read", "audit.read");
            default -> Set.of(
                "inventory.read",
                "order.read", "order.create",
                "approval.read", "approval.request",
                "workflow.hospital.consume", "workflow.ecommerce.exchange"
            );
        };
    }

    public boolean hasScope(String role, String scope) {
        Set<String> scopes = scopesForRole(role);
        return scopes.contains("*") || scopes.contains(scope);
    }

    public Set<String> authoritiesForRole(String role) {
        Set<String> authorities = new LinkedHashSet<>();
        String normalized = role == null ? "STAFF" : role.trim().toUpperCase();
        authorities.add("ROLE_" + normalized);
        for (String scope : scopesForRole(normalized)) {
            if (!"*".equals(scope)) {
                authorities.add("SCOPE_" + scope);
            }
        }
        return authorities;
    }
}
